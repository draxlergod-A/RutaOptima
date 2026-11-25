"""Funciones pequeñas que usan varios módulos."""

from __future__ import annotations

import math

from .modelos import Instancia


def distancia_euclidiana(x1: float, y1: float, x2: float, y2: float) -> float:
    """Distancia en línea recta (km)."""
    return math.hypot(x1 - x2, y1 - y2)


def matriz_aproximada(inst: Instancia) -> list[list[float]]:
    """Matriz de distancias (km) APROXIMADA: línea recta x factor vial.

    Sirve para probar tu módulo sin esperar al ROL 3. La matriz "oficial" del proyecto
    es `distancias.matriz_distancias` (Dijkstra, ROL 3).
    """
    puntos = [inst.deposito] + inst.clientes
    return [
        [
            distancia_euclidiana(a.x, a.y, b.x, b.y) * inst.factor_vial if a.id != b.id else 0.0
            for b in puntos
        ]
        for a in puntos
    ]


def a_tiempos(dist: list[list[float]], velocidad_kmh: float) -> list[list[float]]:
    """Convierte una matriz de distancias (km) en una de tiempos de viaje (minutos)."""
    return [[d / velocidad_kmh * 60.0 for d in fila] for fila in dist]


def hhmm(minutos: float) -> str:
    """540 -> '09:00' (para mostrar horas al usuario)."""
    total = int(round(minutos))
    return f"{total // 60:02d}:{total % 60:02d}"
