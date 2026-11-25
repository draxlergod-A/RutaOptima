"""ROL 7 - Fuerza bruta: prueba TODOS los órdenes. Lento (k!), pero sirve para verificar Held-Karp."""

from __future__ import annotations

import itertools

from .evaluador import evaluar_orden
from .modelos import Cliente, Instancia


def mejor_orden_fuerza_bruta(
    clientes: list[Cliente],
    inst: Instancia,
    tiempos: list[list[float]],
    origen: int = 0,
    t_inicio: float | None = None,
) -> tuple[list[int], float] | None:
    """Mismo problema y mismo resultado que `held_karp.ordenar_zona`, pero con permutaciones."""
    t0 = inst.hora_salida if t_inicio is None else t_inicio
    if not clientes:
        return [], t0
    mejor = None
    for permutacion in itertools.permutations([c.id for c in clientes]):
        orden = list(permutacion)
        t_fin = evaluar_orden(inst, orden, tiempos, origen, t_inicio)   # None si no es factible
        if t_fin is not None and (mejor is None or t_fin < mejor[1]):
            mejor = (orden, t_fin)
    return mejor
