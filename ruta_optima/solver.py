"""Integración (ROL 1): junta las piezas de todos los roles en las dos estrategias.

  Estrategia 1 ("voraz")  : voraz.ruta_voraz
  Estrategia 2 ("dc_pd")  : zonas.dividir_en_zonas  ->  voraz.asignar_zonas  ->  held_karp.ordenar_zona

Este archivo está terminado. Si algo no encaja, avisa al ROL 1.
"""

from __future__ import annotations

import time

from . import config, distancias, held_karp, voraz, zonas
from .evaluador import Evaluacion, evaluar
from .modelos import Instancia, Solucion
from .utilidades import a_tiempos


def preparar(inst: Instancia) -> tuple[list[list[float]], list[list[float]]]:
    """Calcula las matrices (distancias en km, tiempos en minutos) de la instancia."""
    dist = distancias.matriz_distancias(inst)
    return dist, a_tiempos(dist, inst.velocidad_kmh)


def resolver_estrategia_1(
    inst: Instancia,
    dist: list[list[float]] | None = None,
    tiempos: list[list[float]] | None = None,
) -> Solucion:
    """Estrategia 1: vecino más cercano (voraz)."""
    if dist is None or tiempos is None:
        dist, tiempos = preparar(inst)
    t0 = time.perf_counter()
    sol = voraz.ruta_voraz(inst, dist, tiempos)
    sol.nombre = "voraz"
    sol.tiempo_ejecucion_s = time.perf_counter() - t0
    return sol


def resolver_estrategia_2(
    inst: Instancia,
    k: int = config.K_ZONA,
    dist: list[list[float]] | None = None,
    tiempos: list[list[float]] | None = None,
) -> Solucion:
    """Estrategia 2: divide y vencerás (zonas) + voraz (asignación) + Held-Karp (orden)."""
    if dist is None or tiempos is None:
        dist, tiempos = preparar(inst)
    t0 = time.perf_counter()

    todas_las_zonas = zonas.dividir_en_zonas(inst.clientes, k)
    asignacion, sin_cupo = voraz.asignar_zonas(todas_las_zonas, inst, tiempos)

    rutas: list[list[int]] = []
    no_atendidos: list[int] = [c.id for c in sin_cupo]

    for zonas_del_vehiculo in asignacion:
        ruta: list[int] = []
        origen, t = 0, inst.hora_salida
        pendientes = list(zonas_del_vehiculo)
        while pendientes:
            zona = pendientes.pop(0)
            res = held_karp.ordenar_zona(zona, inst, tiempos, origen, t)
            if res is None:
                # La zona completa no es factible: se parte en mitades y se reintenta.
                if len(zona) > 1:
                    mitades = zonas.dividir_en_zonas(zona, max(1, len(zona) // 2))
                    pendientes = mitades + pendientes
                else:
                    no_atendidos.append(zona[0].id)
                continue
            orden, t = res
            ruta.extend(orden)
            origen = orden[-1] if orden else origen
        if ruta:
            rutas.append(ruta)

    sol = Solucion("dc_pd", rutas, sorted(no_atendidos))
    sol.tiempo_ejecucion_s = time.perf_counter() - t0
    return sol


def comparar(
    inst: Instancia, k: int = config.K_ZONA
) -> dict[str, tuple[Solucion, Evaluacion]]:
    """Corre las dos estrategias sobre la misma instancia y las evalúa.

    Devuelve {"voraz": (solucion, evaluacion), "dc_pd": (solucion, evaluacion)}.
    """
    dist, tiempos = preparar(inst)
    resultado: dict[str, tuple[Solucion, Evaluacion]] = {}
    s1 = resolver_estrategia_1(inst, dist, tiempos)
    resultado["voraz"] = (s1, evaluar(inst, s1, dist, tiempos))
    s2 = resolver_estrategia_2(inst, k, dist, tiempos)
    resultado["dc_pd"] = (s2, evaluar(inst, s2, dist, tiempos))
    return resultado
