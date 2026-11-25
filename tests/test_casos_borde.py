"""ROL 8 - casos borde del sistema completo. Cada integrante de ROL 8 agrega aquí sus pruebas.

TODO (ROL 8): reemplazar los `pytest.skip` por pruebas reales (ver docs/tareas/ROL-08_*.md).
"""
import pytest

from ruta_optima.generador import generar_instancia
from ruta_optima.solver import comparar
from tests.ayudas import llamar


def test_un_solo_cliente():
    inst = generar_instancia(1, 2, semilla=1)
    r = llamar(comparar, inst, 12)
    assert all(ev.valida for _, ev in r.values())


def test_exactamente_k_clientes():
    inst = generar_instancia(12, 2, semilla=1)
    r = llamar(comparar, inst, 12)
    assert all(ev.valida for _, ev in r.values())


def test_k_mas_uno_clientes():
    inst = generar_instancia(13, 2, semilla=1)
    r = llamar(comparar, inst, 12)
    assert all(ev.valida for _, ev in r.values())


@pytest.mark.skip(reason="TODO ROL 8: capacidad total insuficiente -> debe haber no_atendidos")
def test_capacidad_insuficiente():
    ...


@pytest.mark.skip(reason="TODO ROL 8: ventana imposible de cumplir")
def test_ventanas_imposibles():
    ...
