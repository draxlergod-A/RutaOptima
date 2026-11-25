"""ROL 6 - Programación dinámica (Held-Karp): el mejor orden EXACTO para visitar una zona."""

from __future__ import annotations

import math

from .modelos import Cliente, Instancia


def ordenar_zona(
    clientes: list[Cliente],
    inst: Instancia,
    tiempos: list[list[float]],
    origen: int = 0,
    t_inicio: float | None = None,
) -> tuple[list[int], float] | None:
    """Mejor orden para visitar a todos los clientes de la zona: el que termina más temprano.

    dp[mascara][j] = menor instante en que se puede terminar de atender al cliente j habiendo
    atendido exactamente los clientes de `mascara` (un número cuyos bits indican cuáles).
    Complejidad O(k^2 * 2^k) en tiempo y O(k * 2^k) en memoria (k = len(clientes)).

    Devuelve (orden de ids, instante en que termina el último servicio) o None si ningún orden
    cumple las ventanas de tiempo y la jornada.
    """
    t0 = inst.hora_salida if t_inicio is None else t_inicio
    k = len(clientes)
    if k == 0:
        return [], t0

    INF = math.inf
    ids = [c.id for c in clientes]
    total = 1 << k                                         # 2^k subconjuntos
    dp = [[INF] * k for _ in range(total)]
    padre = [[-1] * k for _ in range(total)]               # para reconstruir el orden

    # Caso base: ir directo del origen a cada cliente j.
    for j, c in enumerate(clientes):
        inicio = max(t0 + tiempos[origen][c.id], c.ventana_ini)   # si llega antes, espera
        if inicio <= c.ventana_fin:                               # ¿llega a tiempo?
            dp[1 << j][j] = inicio + c.servicio

    # Transición: agregar un cliente i que aún no está en la máscara.
    for mascara in range(1, total):
        for j in range(k):
            t = dp[mascara][j]
            if t == INF:
                continue
            for i in range(k):
                if mascara >> i & 1:                          # i ya fue atendido
                    continue
                c = clientes[i]
                inicio = max(t + tiempos[ids[j]][c.id], c.ventana_ini)
                if inicio > c.ventana_fin:                    # llegaría tarde: descartar
                    continue
                nueva = mascara | (1 << i)
                if inicio + c.servicio < dp[nueva][i]:
                    dp[nueva][i] = inicio + c.servicio
                    padre[nueva][i] = j

    # Mejor final: el que termina antes y todavía alcanza a volver al almacén en la jornada.
    completa = total - 1
    mejor = None
    for j in range(k):
        t = dp[completa][j]
        if t < INF and t + tiempos[ids[j]][0] <= inst.hora_limite + 1e-9:
            if mejor is None or t < mejor[0]:
                mejor = (t, j)
    if mejor is None:
        return None

    # Reconstrucción hacia atrás usando `padre`.
    t_fin, j = mejor
    orden, mascara = [], completa
    while j != -1:
        orden.append(ids[j])
        anterior = padre[mascara][j]
        mascara ^= 1 << j
        j = anterior
    return orden[::-1], t_fin
