"""ROL 7 - fuerza_bruta.py (verificación del Held-Karp)"""
import pytest

from ruta_optima import fuerza_bruta as m
from ruta_optima.generador import generar_instancia
from ruta_optima.utilidades import a_tiempos, matriz_aproximada
from tests.ayudas import fuerza_bruta_local, instancia_manual, llamar, matriz_lineal


def test_ejemplo_a_mano():
    inst = instancia_manual([(600, 720), (540, 560)])
    _, tiempos = matriz_lineal(2)
    orden, t_fin = llamar(m.mejor_orden_fuerza_bruta, inst.clientes, inst, tiempos)
    assert orden == [2, 1] and t_fin == pytest.approx(605)


def test_infactible_y_vacio():
    inst = instancia_manual([(540, 545)])
    _, tiempos = matriz_lineal(1)
    assert llamar(m.mejor_orden_fuerza_bruta, inst.clientes, inst, tiempos) is None
    assert m.mejor_orden_fuerza_bruta([], inst, tiempos, 0, 600) == ([], 600)


def test_coincide_con_la_copia_de_las_pruebas():
    inst = generar_instancia(20, 2, semilla=3)
    tiempos = a_tiempos(matriz_aproximada(inst), inst.velocidad_kmh)
    zona = inst.clientes[:6]
    a = llamar(m.mejor_orden_fuerza_bruta, zona, inst, tiempos)
    b = fuerza_bruta_local(inst, zona, tiempos)
    assert (a is None) == (b is None)
    if a:
        assert a[1] == pytest.approx(b[1])
