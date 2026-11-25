"""Funciones de ayuda para las pruebas (no son pruebas)."""

from __future__ import annotations

import itertools

import pytest

from ruta_optima.evaluador import evaluar_orden
from ruta_optima.modelos import Cliente, Instancia


def llamar(funcion, *args, **kwargs):
    """Llama a `funcion`; si todavía está pendiente (NotImplementedError), SALTA la prueba.

    Así una prueba solo falla cuando el módulo YA está programado pero tiene un error.
    """
    try:
        return funcion(*args, **kwargs)
    except NotImplementedError as e:
        pytest.skip(str(e))


def instancia_manual(
    ventanas: list[tuple[float, float]],
    servicios: float | list[float] = 5,
    demandas: int | list[int] = 1,
    jornada: float = 480,
    hora_salida: float = 540,
    capacidad: int = 100,
    num_vehiculos: int = 1,
) -> Instancia:
    """Instancia pequeña hecha a mano. `ventanas[i]` es (inicio, fin) del cliente i+1."""
    deposito = Cliente(0, 0.0, 0.0, 0, 0.0, 1440.0, 0.0)
    clientes = []
    for i, (ini, fin) in enumerate(ventanas):
        s = servicios[i] if isinstance(servicios, list) else servicios
        d = demandas[i] if isinstance(demandas, list) else demandas
        clientes.append(Cliente(i + 1, float(i + 1), 0.0, d, float(ini), float(fin), float(s)))
    return Instancia(deposito, clientes, num_vehiculos, capacidad=capacidad,
                     jornada_max=jornada, hora_salida=hora_salida)


def matriz_lineal(n: int, paso_min: float = 10.0, km_por_paso: float = 2.0):
    """Puntos en una línea: el almacén es el 0 y el cliente i está a i pasos.

    Devuelve (dist, tiempos): tiempos[i][j] = |i - j| * paso_min minutos.
    """
    tiempos = [[abs(i - j) * paso_min for j in range(n + 1)] for i in range(n + 1)]
    dist = [[abs(i - j) * km_por_paso for j in range(n + 1)] for i in range(n + 1)]
    return dist, tiempos


def fuerza_bruta_local(inst, clientes, tiempos, origen=0, t_inicio=None):
    """Mejor orden probando todas las permutaciones (copia propia para no depender del ROL 7)."""
    t0 = inst.hora_salida if t_inicio is None else t_inicio
    if not clientes:
        return [], t0
    mejor = None
    for perm in itertools.permutations([c.id for c in clientes]):
        t = evaluar_orden(inst, list(perm), tiempos, origen, t_inicio)
        if t is not None and (mejor is None or t < mejor[1]):
            mejor = (list(perm), t)
    return mejor
