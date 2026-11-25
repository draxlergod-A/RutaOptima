"""Evaluador: la "regla única" del proyecto.

Aquí se define cómo se calcula el tiempo, el costo y si una solución cumple las restricciones.
Todos los algoritmos y las pruebas usan estas mismas funciones, así que nadie puede
interpretar las reglas distinto.

Reglas de tiempo (se repiten en todo el proyecto):
  * El vehículo sale del almacén en `inst.hora_salida` (09:00).
  * Al llegar a un cliente: inicio_servicio = max(llegada, ventana_ini).
    Si llega antes de que abra la ventana, ESPERA.
  * Si inicio_servicio > ventana_fin, la ruta NO es válida (llegó tarde).
  * Después del servicio (`servicio` minutos) sale hacia el siguiente cliente.
  * Al final regresa al almacén y debe llegar antes de `inst.hora_salida + inst.jornada_max`.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from . import config
from .modelos import Instancia, Solucion


# ---------------------------------------------------------------------------
# Función clave para los algoritmos de ordenamiento (ROL 5, 6 y 7)
# ---------------------------------------------------------------------------
def evaluar_orden(
    inst: Instancia,
    orden: list[int],
    tiempos: list[list[float]],
    origen: int = 0,
    t_inicio: float | None = None,
) -> float | None:
    """Simula visitar los clientes de `orden` (ids) partiendo de `origen` en `t_inicio`.

    Devuelve el instante en que TERMINA el servicio del último cliente, o None si el orden
    no es factible (llega tarde a alguna ventana, o no alcanza a volver al almacén a tiempo).

    Si `orden` está vacío devuelve `t_inicio` (o la hora de salida si no se indica).
    """
    t = inst.hora_salida if t_inicio is None else t_inicio
    actual = origen
    for cid in orden:
        c = inst.cliente(cid)
        llegada = t + tiempos[actual][cid]
        inicio = max(llegada, c.ventana_ini)
        if inicio > c.ventana_fin + config.EPS:
            return None
        t = inicio + c.servicio
        actual = cid
    if orden and t + tiempos[actual][0] > inst.hora_limite + config.EPS:
        return None
    return t


# ---------------------------------------------------------------------------
# Simulación detallada de una ruta
# ---------------------------------------------------------------------------
@dataclass
class ResultadoRuta:
    factible: bool
    distancia_km: float = 0.0
    duracion_min: float = 0.0          # desde la salida hasta volver al almacén
    carga: int = 0
    paradas: list[tuple[int, float, float]] = field(default_factory=list)  # (id, llegada, inicio)
    errores: list[str] = field(default_factory=list)


def simular_ruta(
    inst: Instancia,
    ruta: list[int],
    dist: list[list[float]],
    tiempos: list[list[float]],
) -> ResultadoRuta:
    """Recorre una ruta completa (almacén -> clientes -> almacén) y reporta qué pasó."""
    res = ResultadoRuta(factible=True)
    if not ruta:
        return res

    t = inst.hora_salida
    actual = 0
    for cid in ruta:
        c = inst.cliente(cid)
        res.distancia_km += dist[actual][cid]
        llegada = t + tiempos[actual][cid]
        inicio = max(llegada, c.ventana_ini)
        res.paradas.append((cid, llegada, inicio))
        if inicio > c.ventana_fin + config.EPS:
            res.errores.append(
                f"Cliente {cid}: llega a las {llegada:.1f} min y su ventana cierra a las {c.ventana_fin:.0f}"
            )
        res.carga += c.demanda
        t = inicio + c.servicio
        actual = cid

    res.distancia_km += dist[actual][0]
    t += tiempos[actual][0]
    res.duracion_min = t - inst.hora_salida

    if res.carga > inst.capacidad:
        res.errores.append(f"Carga {res.carga} supera la capacidad {inst.capacidad}")
    if t > inst.hora_limite + config.EPS:
        res.errores.append(
            f"Vuelve al almacén en el minuto {t:.1f} y la jornada termina en {inst.hora_limite:.0f}"
        )
    res.factible = not res.errores
    return res


# ---------------------------------------------------------------------------
# Evaluación de una solución completa
# ---------------------------------------------------------------------------
@dataclass
class Evaluacion:
    valida: bool
    errores: list[str]
    costo_total: float          # S/ = costo_km * km + costo_hora * horas
    distancia_km: float
    horas_operacion: float
    vehiculos_usados: int
    atendidos: int
    no_atendidos: int
    pct_atendidos: float        # 0 a 100


def evaluar(
    inst: Instancia,
    sol: Solucion,
    dist: list[list[float]],
    tiempos: list[list[float]],
) -> Evaluacion:
    """Verifica TODAS las restricciones de una solución y calcula su costo."""
    errores: list[str] = []

    rutas = [r for r in sol.rutas if r]
    if len(rutas) > inst.num_vehiculos:
        errores.append(f"Usa {len(rutas)} vehículos y la flota tiene {inst.num_vehiculos}")

    # Cada cliente: exactamente una vez (en una ruta o en no_atendidos)
    vistos: dict[int, int] = {}
    for ruta in rutas:
        for cid in ruta:
            vistos[cid] = vistos.get(cid, 0) + 1
    for cid in sol.no_atendidos:
        vistos[cid] = vistos.get(cid, 0) + 1
    ids_validos = {c.id for c in inst.clientes}
    for cid, veces in vistos.items():
        if cid not in ids_validos:
            errores.append(f"El id {cid} no existe en la instancia")
        elif veces > 1:
            errores.append(f"El cliente {cid} aparece {veces} veces")
    faltan = sorted(ids_validos - set(vistos))
    if faltan:
        errores.append(f"Clientes que no están en ninguna ruta ni en no_atendidos: {faltan[:10]}")

    dist_total = 0.0
    min_total = 0.0
    atendidos = 0
    for k, ruta in enumerate(rutas, start=1):
        if any(cid not in ids_validos for cid in ruta):
            continue  # ya se reportó el id inválido
        r = simular_ruta(inst, ruta, dist, tiempos)
        dist_total += r.distancia_km
        min_total += r.duracion_min
        atendidos += len(ruta)
        errores.extend(f"Ruta {k}: {e}" for e in r.errores)

    horas = min_total / 60.0
    n = inst.n
    return Evaluacion(
        valida=not errores,
        errores=errores,
        costo_total=inst.costo_km * dist_total + inst.costo_hora * horas,
        distancia_km=dist_total,
        horas_operacion=horas,
        vehiculos_usados=len(rutas),
        atendidos=atendidos,
        no_atendidos=len(set(sol.no_atendidos) & ids_validos),
        pct_atendidos=100.0 * atendidos / n if n else 100.0,
    )
