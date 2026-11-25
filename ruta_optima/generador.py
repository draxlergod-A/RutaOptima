"""Generador de instancias aleatorias (casos de prueba repetibles).

Con la misma semilla siempre se obtiene la misma instancia.
El ROL 2 puede mejorar/ampliar esto en `instancias.py` (no es necesario tocar este archivo).
"""

from __future__ import annotations

import math
import random

from . import config
from .modelos import Cliente, Instancia


def vehiculos_por_defecto(n: int) -> int:
    """Cantidad de vehículos que se usa si no se indica: unos 7 clientes por vehículo (con 12 no alcanza el tiempo
    para atender a casi nadie: se probó con una solución de referencia)."""
    return max(2, min(config.FLOTA_MAX, math.ceil(n / 7)))


def generar_instancia(
    n: int,
    num_vehiculos: int | None = None,
    semilla: int = config.SEMILLA_DEFECTO,
) -> Instancia:
    """Crea una instancia con `n` clientes repartidos al azar en la ciudad simulada.

    Args:
        n: número de clientes (el proyecto usa de 20 a 200; para pruebas se aceptan menos).
        num_vehiculos: tamaño de la flota; si es None se calcula con `vehiculos_por_defecto`.
        semilla: semilla del generador aleatorio.
    """
    if n < 1:
        raise ValueError("n debe ser al menos 1")
    rng = random.Random(semilla)
    centro = config.AREA_KM / 2
    deposito = Cliente(0, centro, centro, 0, 0.0, 24 * 60.0, 0.0)

    clientes: list[Cliente] = []
    for i in range(1, n + 1):
        inicio = rng.randrange(
            config.VENTANA_INICIO_MIN, config.VENTANA_INICIO_MAX + 1, config.VENTANA_PASO_MIN
        )
        clientes.append(
            Cliente(
                id=i,
                x=round(rng.uniform(0, config.AREA_KM), 3),
                y=round(rng.uniform(0, config.AREA_KM), 3),
                demanda=rng.randint(*config.DEMANDA_RANGO),
                ventana_ini=float(inicio),
                ventana_fin=float(inicio + config.VENTANA_DURACION_MIN),
                servicio=float(rng.randint(*config.SERVICIO_RANGO_MIN)),
            )
        )

    m = vehiculos_por_defecto(n) if num_vehiculos is None else num_vehiculos
    return Instancia(deposito=deposito, clientes=clientes, num_vehiculos=m, semilla=semilla)
