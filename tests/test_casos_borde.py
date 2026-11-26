"""ROL 8 - casos borde del sistema completo: casos pequeños, capacidad insuficiente y ventanas imposibles."""

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


def test_capacidad_insuficiente():
    from ruta_optima.modelos import Instancia
    base = generar_instancia(20, 2, semilla=1)
    inst = Instancia(base.deposito, base.clientes, 2, capacidad=10)   # capacidad total 20 < demanda
    for nombre, (sol, ev) in comparar(inst, 12).items():
        assert ev.valida, (nombre, ev.errores)
        assert ev.no_atendidos > 0


def test_ventanas_imposibles():
    from dataclasses import replace
    from ruta_optima.modelos import Instancia
    base = generar_instancia(10, 3, semilla=1)
    clientes = [replace(c, ventana_ini=0.0, ventana_fin=1.0) for c in base.clientes]  # cierran a las 00:01
    inst = Instancia(base.deposito, clientes, 3)
    for nombre, (sol, ev) in comparar(inst, 12).items():
        assert ev.valida, (nombre, ev.errores)
        assert ev.atendidos == 0
