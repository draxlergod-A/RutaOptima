"""ROL 3 - distancias.py"""
import math

import pytest

from ruta_optima import distancias as m
from ruta_optima.generador import generar_instancia
from tests.ayudas import llamar


def test_dijkstra_ejemplo_de_la_documentacion():
    grafo = {0: [(1, 4.0), (2, 1.0)], 1: [(0, 4.0), (2, 2.0), (3, 5.0)],
             2: [(0, 1.0), (1, 2.0)], 3: [(1, 5.0)]}
    assert llamar(m.dijkstra, grafo, 0) == {0: 0.0, 1: 3.0, 2: 1.0, 3: 8.0}


def test_dijkstra_grafo_dirigido():
    grafo = {0: [(1, 4), (2, 1)], 2: [(1, 2), (3, 7)], 1: [(3, 5)], 3: []}
    assert llamar(m.dijkstra, grafo, 0) == {0: 0, 2: 1, 1: 3, 3: 8}


def test_dijkstra_nodo_inalcanzable():
    grafo = {0: [(1, 1)], 1: [], 2: []}
    d = llamar(m.dijkstra, grafo, 0)
    assert d[2] == math.inf


def test_matriz_distancias_propiedades():
    inst = generar_instancia(10, 2, semilla=4)
    d = llamar(m.matriz_distancias, inst)
    n = inst.n + 1
    assert len(d) == n and all(len(f) == n for f in d)
    for i in range(n):
        assert d[i][i] == 0
        for j in range(n):
            assert d[i][j] == pytest.approx(d[j][i])
            euclid = math.hypot(inst.cliente(i).x - inst.cliente(j).x,
                                inst.cliente(i).y - inst.cliente(j).y)
            assert d[i][j] >= euclid - 1e-6
            for k in range(n):
                assert d[i][j] <= d[i][k] + d[k][j] + 1e-6
