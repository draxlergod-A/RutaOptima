"""ROL 3 - Distancias reales con Dijkstra sobre una red de calles simulada.

La ciudad se modela como una cuadrícula de calles (una intersección cada 1 km). Cada cliente
se "engancha" a la intersección más cercana. Dijkstra calcula el camino mínimo por las calles.
"""

from __future__ import annotations

import heapq
import math

from . import config
from .modelos import Instancia

# Grafo = diccionario de adyacencia: {nodo: [(vecino, peso_km), ...]}
Grafo = dict[int, list[tuple[int, float]]]


def dijkstra(grafo: Grafo, origen: int) -> dict[int, float]:
    """Camino mínimo desde `origen` hacia todos los nodos. Complejidad O((V + E) log V)."""
    dist = {nodo: math.inf for nodo in grafo}
    dist[origen] = 0.0
    cola = [(0.0, origen)]                    # cola de prioridad (min-heap) de (distancia, nodo)
    while cola:
        d, u = heapq.heappop(cola)
        if d > dist[u]:                        # entrada vieja: ya hay un camino mejor
            continue
        for v, peso in grafo.get(u, []):
            nueva = d + peso
            if nueva < dist.get(v, math.inf):  # relajación de la arista (u, v)
                dist[v] = nueva
                heapq.heappush(cola, (nueva, v))
    return dist


def construir_grafo_calles(inst: Instancia) -> tuple[Grafo, dict[int, int]]:
    """Cuadrícula de calles de 1 km + conexión de cada cliente a su intersección más cercana.

    Devuelve (grafo, nodo_de_cliente) donde nodo_de_cliente[id] es el nodo del cliente `id`.
    """
    lado = int(config.AREA_KM)
    m = lado + 1                               # intersecciones por lado

    def nodo(i: int, j: int) -> int:
        return i * m + j

    grafo: Grafo = {nodo(i, j): [] for i in range(m) for j in range(m)}
    for i in range(m):
        for j in range(m):
            for di, dj in ((1, 0), (0, 1)):   # calle hacia el este y hacia el norte
                a, b = i + di, j + dj
                if a < m and b < m:
                    grafo[nodo(i, j)].append((nodo(a, b), 1.0))
                    grafo[nodo(a, b)].append((nodo(i, j), 1.0))

    nodo_de_cliente: dict[int, int] = {}
    siguiente = m * m
    for c in [inst.deposito] + inst.clientes:
        i = min(lado, max(0, round(c.x)))      # intersección más cercana
        j = min(lado, max(0, round(c.y)))
        peso = math.hypot(c.x - i, c.y - j)    # tramo "de la puerta a la esquina"
        nodo_de_cliente[c.id] = siguiente
        grafo[siguiente] = [(nodo(i, j), peso)]
        grafo[nodo(i, j)].append((siguiente, peso))
        siguiente += 1
    return grafo, nodo_de_cliente


def matriz_distancias(inst: Instancia) -> list[list[float]]:
    """Matriz (n+1)x(n+1) de km mínimos entre almacén y clientes (indexada por id)."""
    grafo, nodo_de = construir_grafo_calles(inst)
    n = inst.n + 1
    matriz = [[0.0] * n for _ in range(n)]
    for i in range(n):
        d = dijkstra(grafo, nodo_de[i])        # un Dijkstra por cada cliente y el almacén
        for j in range(n):
            matriz[i][j] = d[nodo_de[j]]
    return matriz
