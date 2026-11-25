"""Página web del proyecto (ROL 9 la puede mejorar).

Para abrirla:   python app.py        y luego entra a  http://localhost:8000
(No necesita instalar nada extra: usa solo Python. La página está en la carpeta web/.)

Cómo funciona: este archivo es un servidor pequeño. La página (web/index.html + estilos.css +
app.js) le manda los parámetros a  POST /api/resolver  y el servidor corre los algoritmos REALES
del proyecto (ruta_optima/) y devuelve las rutas en JSON para dibujarlas.
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from ruta_optima import config
from ruta_optima.evaluador import simular_ruta
from ruta_optima.generador import generar_instancia, vehiculos_por_defecto
from ruta_optima.instancias import generar_instancia_distritos
from ruta_optima.solver import preparar, resolver_estrategia_1, resolver_estrategia_2
from ruta_optima.evaluador import evaluar
from ruta_optima.utilidades import hhmm
from ruta_optima.zonas import dividir_en_zonas

RAIZ = os.path.dirname(os.path.abspath(__file__))
CARPETA_WEB = os.path.join(RAIZ, "web")
CARPETA_RESULTADOS = os.path.join(RAIZ, "resultados")


def _entero(datos: dict, clave: str, defecto: int, minimo: int, maximo: int) -> int:
    """Lee un número entero del JSON y lo limita al rango permitido."""
    try:
        valor = int(datos.get(clave, defecto))
    except (TypeError, ValueError):
        valor = defecto
    return max(minimo, min(maximo, valor))


def resolver(datos: dict) -> dict:
    """Genera la instancia, corre las dos estrategias y arma la respuesta para la página."""
    n = _entero(datos, "n", 40, 1, config.N_MAX)
    vehiculos = _entero(datos, "vehiculos", vehiculos_por_defecto(n), 1, config.FLOTA_MAX)
    k = _entero(datos, "k", config.K_ZONA, 2, 14)
    semilla = _entero(datos, "semilla", config.SEMILLA_DEFECTO, 0, 10**6)
    distritos = bool(datos.get("distritos", False))

    inst = (generar_instancia_distritos if distritos else generar_instancia)(n, vehiculos, semilla)
    dist, tiempos = preparar(inst)

    soluciones = {
        "voraz": resolver_estrategia_1(inst, dist, tiempos),
        "dc_pd": resolver_estrategia_2(inst, k, dist, tiempos),
    }
    resultados = {}
    for nombre, sol in soluciones.items():
        ev = evaluar(inst, sol, dist, tiempos)
        rutas = []
        for i, ruta in enumerate(sol.rutas, 1):
            sim = simular_ruta(inst, ruta, dist, tiempos)
            paradas = []
            for cid, llegada, inicio in sim.paradas:
                c = inst.cliente(cid)
                paradas.append({
                    "id": cid, "llegada": hhmm(llegada), "inicio": hhmm(inicio),
                    "ventana": f"{hhmm(c.ventana_ini)}–{hhmm(c.ventana_fin)}",
                    "espera_min": round(max(0.0, inicio - llegada)),
                })
            rutas.append({
                "vehiculo": i, "carga": sim.carga, "km": round(sim.distancia_km, 1),
                "duracion_h": round(sim.duracion_min / 60, 2), "clientes": ruta,
                "paradas": paradas,
            })
        resultados[nombre] = {
            "valida": ev.valida, "errores": ev.errores[:10],
            "metricas": {
                "costo": round(ev.costo_total, 2), "km": round(ev.distancia_km, 1),
                "horas": round(ev.horas_operacion, 1), "vehiculos": ev.vehiculos_usados,
                "atendidos": ev.atendidos, "no_atendidos": ev.no_atendidos,
                "pct": round(ev.pct_atendidos, 1),
                "segundos": round(sol.tiempo_ejecucion_s, 4),
            },
            "rutas": rutas, "no_atendidos": sol.no_atendidos,
        }

    zonas = [[c.id for c in z] for z in dividir_en_zonas(inst.clientes, k)]
    return {
        "instancia": {
            "n": inst.n, "vehiculos": inst.num_vehiculos, "capacidad": inst.capacidad,
            "area_km": config.AREA_KM, "hora_salida": hhmm(inst.hora_salida),
            "hora_limite": hhmm(inst.hora_limite), "k": k, "semilla": semilla,
            "deposito": {"x": inst.deposito.x, "y": inst.deposito.y},
            "clientes": [{
                "id": c.id, "x": round(c.x, 3), "y": round(c.y, 3), "demanda": c.demanda,
                "ventana": f"{hhmm(c.ventana_ini)}–{hhmm(c.ventana_fin)}", "servicio": c.servicio,
            } for c in inst.clientes],
        },
        "zonas": zonas,
        "resultados": resultados,
    }


class Manejador(BaseHTTPRequestHandler):
    """Atiende la página (archivos de web/ y resultados/) y la API."""

    def _enviar(self, codigo: int, contenido: bytes, tipo: str) -> None:
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(contenido)))
        self.end_headers()
        self.wfile.write(contenido)

    def _json(self, codigo: int, objeto: dict) -> None:
        self._enviar(codigo, json.dumps(objeto, ensure_ascii=False).encode("utf-8"),
                     "application/json; charset=utf-8")

    def do_GET(self) -> None:  # noqa: N802 (nombre exigido por http.server)
        ruta = urlparse(self.path).path
        if ruta == "/api/graficos":                  # lista de gráficos del benchmark
            archivos = []
            if os.path.isdir(CARPETA_RESULTADOS):
                archivos = sorted(f for f in os.listdir(CARPETA_RESULTADOS) if f.endswith(".png"))
            self._json(200, {"graficos": archivos})
            return
        if ruta == "/":
            ruta = "/index.html"
        if ruta.startswith("/resultados/"):
            base, relativa = CARPETA_RESULTADOS, ruta[len("/resultados/"):]
        else:
            base, relativa = CARPETA_WEB, ruta.lstrip("/")
        archivo = os.path.normpath(os.path.join(base, relativa))
        if not archivo.startswith(base) or not os.path.isfile(archivo):   # evita salir de la carpeta
            self._enviar(404, b"No encontrado", "text/plain; charset=utf-8")
            return
        tipo = mimetypes.guess_type(archivo)[0] or "application/octet-stream"
        if tipo.startswith("text/") or tipo in ("application/javascript", "application/json"):
            tipo += "; charset=utf-8"
        with open(archivo, "rb") as f:
            self._enviar(200, f.read(), tipo)

    def do_POST(self) -> None:  # noqa: N802
        if urlparse(self.path).path != "/api/resolver":
            self._json(404, {"error": "ruta desconocida"})
            return
        try:
            largo = int(self.headers.get("Content-Length", 0))
            datos = json.loads(self.rfile.read(largo) or b"{}")
            self._json(200, resolver(datos))
        except Exception as error:  # la página muestra el mensaje en vez de romperse
            self._json(500, {"error": f"{type(error).__name__}: {error}"})

    def log_message(self, formato, *args) -> None:   # silencia el registro por petición
        pass


def main() -> None:
    parser = argparse.ArgumentParser(description="Servidor de la página web del proyecto")
    parser.add_argument("--puerto", type=int, default=8000)
    parser.add_argument("--sin-navegador", action="store_true")
    args = parser.parse_args()
    servidor = ThreadingHTTPServer(("127.0.0.1", args.puerto), Manejador)
    url = f"http://localhost:{args.puerto}"
    print(f"Página lista en {url}   (Ctrl+C para detener)")
    if not args.sin_navegador:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")


if __name__ == "__main__":
    main()
