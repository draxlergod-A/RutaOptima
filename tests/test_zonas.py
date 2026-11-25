"""ROL 4 - zonas.py"""
import math
import random

import pytest

from ruta_optima import zonas as m
from ruta_optima.generador import generar_instancia
from tests.ayudas import llamar


def test_quickselect_contra_sorted():
    rnd = random.Random(0)
    for _ in range(50):
        v = [rnd.randint(0, 20) for _ in range(rnd.randint(1, 30))]
        k = rnd.randrange(len(v))
        copia = list(v)
        assert llamar(m.quickselect, v, k) == sorted(v)[k]
        assert v == copia  # no modifica la lista original


@pytest.mark.parametrize("n,k", [(20, 12), (50, 12), (200, 12), (37, 5), (13, 12)])
def test_dividir_en_zonas_propiedades(n, k):
    inst = generar_instancia(n, 3, semilla=7)
    antes = list(inst.clientes)
    zonas = llamar(m.dividir_en_zonas, inst.clientes, k)
    ids = sorted(c.id for z in zonas for c in z)
    assert ids == sorted(c.id for c in inst.clientes)          # partición exacta
    assert all(1 <= len(z) <= k for z in zonas)
    assert len(zonas) <= 2 * math.ceil(n / k)
    assert inst.clientes == antes                               # no muta la entrada
    assert zonas == m.dividir_en_zonas(inst.clientes, k)        # determinista


def test_casos_borde():
    assert llamar(m.dividir_en_zonas, [], 12) == []
    inst = generar_instancia(5, 1)
    with pytest.raises(ValueError):
        m.dividir_en_zonas(inst.clientes, 0)
