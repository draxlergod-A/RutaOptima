"""Tablero automático: dice qué módulos ya están programados y cuáles faltan.

Se usa con:   python main.py --estado
Prueba cada módulo con una instancia diminuta: si lanza NotImplementedError, está pendiente.
"""

from __future__ import annotations

from . import benchmark, distancias, fuerza_bruta, held_karp, instancias, voraz, zonas
from .generador import generar_instancia
from .utilidades import a_tiempos, matriz_aproximada


def _sondas():
    inst = generar_instancia(6, 2, semilla=0)
    dist = matriz_aproximada(inst)
    tiempos = a_tiempos(dist, inst.velocidad_kmh)
    mitad = [inst.clientes[:3], inst.clientes[3:]]
    return [
        (2, "instancias.py", lambda: instancias.instancias_de_prueba()),
        (3, "distancias.py", lambda: distancias.matriz_distancias(inst)),
        (4, "zonas.py", lambda: zonas.dividir_en_zonas(inst.clientes, 3)),
        (5, "voraz.py", lambda: (voraz.asignar_zonas(mitad, inst, tiempos),
                                 voraz.ruta_voraz(inst, dist, tiempos))),
        (6, "held_karp.py", lambda: held_karp.ordenar_zona(inst.clientes[:4], inst, tiempos)),
        (7, "fuerza_bruta.py", lambda: fuerza_bruta.mejor_orden_fuerza_bruta(
            inst.clientes[:4], inst, tiempos)),
        (8, "benchmark.py", lambda: benchmark.ejecutar_benchmark([6], [0], carpeta=None)),
    ]


def estado_modulos() -> list[dict]:
    """Devuelve una lista de {rol, archivo, estado, detalle}. estado: LISTO / PENDIENTE / ERROR."""
    filas = []
    for rol, archivo, sonda in _sondas():
        try:
            sonda()
            filas.append({"rol": rol, "archivo": archivo, "estado": "LISTO", "detalle": ""})
        except NotImplementedError as e:
            filas.append({"rol": rol, "archivo": archivo, "estado": "PENDIENTE", "detalle": str(e)})
        except Exception as e:  # noqa: BLE001 - queremos mostrar cualquier error al equipo
            filas.append({"rol": rol, "archivo": archivo, "estado": "ERROR",
                          "detalle": f"{type(e).__name__}: {e}"})
    filas.append({"rol": 9, "archivo": "app.py + web/", "estado": "MANUAL",
                  "detalle": "se revisa abriendo: python app.py"})
    filas.append({"rol": 10, "archivo": "docs/ + informe Word", "estado": "MANUAL",
                  "detalle": "se revisa con docs/tareas/ROL-10_informe-final.md"})
    return filas


def imprimir_estado() -> int:
    """Imprime el tablero. Devuelve cuántos módulos están en PENDIENTE o ERROR."""
    filas = estado_modulos()
    print("\nESTADO DEL PROYECTO (se calcula probando el código)")
    print("-" * 78)
    print(f"{'ROL':<4} {'ARCHIVO':<22} {'ESTADO':<10} DETALLE")
    print("-" * 78)
    for f in filas:
        detalle = f["detalle"]
        if len(detalle) > 38:
            detalle = detalle[:35] + "..."
        print(f"{f['rol']:<4} {f['archivo']:<22} {f['estado']:<10} {detalle}")
    print("-" * 78)
    faltan = sum(1 for f in filas if f["estado"] in ("PENDIENTE", "ERROR"))
    print(f"Módulos por terminar: {faltan}\n")
    return faltan
