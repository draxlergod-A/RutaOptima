"""ROL 6 - held_karp.py"""
import random

import pytest

from ruta_optima import held_karp as m
from ruta_optima.generador import generar_instancia
from ruta_optima.utilidades import a_tiempos, matriz_aproximada
from tests.ayudas import fuerza_bruta_local, instancia_manual, llamar, matriz_lineal


def test_ejemplo_a_mano_ventanas_fuerzan_el_orden():
    inst = instancia_manual([(600, 720), (540, 560)])
    _, tiempos = matriz_lineal(2)
    orden, t_fin = llamar(m.ordenar_zona, inst.clientes, inst, tiempos)
    assert orden == [2, 1]
    assert t_fin == pytest.approx(605)


def test_zona_infactible_devuelve_none():
    inst = instancia_manual([(540, 545)])
    _, tiempos = matriz_lineal(1)
    assert llamar(m.ordenar_zona, inst.clientes, inst, tiempos) is None


def test_zona_vacia():
    inst = instancia_manual([(540, 1000)])
    _, tiempos = matriz_lineal(1)
    assert llamar(m.ordenar_zona, [], inst, tiempos, 0, 600) == ([], 600)


def test_jornada_corta_es_infactible():
    inst = instancia_manual([(540, 1000), (540, 1000)], jornada=40)
    _, tiempos = matriz_lineal(2)
    assert llamar(m.ordenar_zona, inst.clientes, inst, tiempos) is None


@pytest.mark.parametrize("semilla", range(15))
def test_igual_que_fuerza_bruta(semilla):
    rnd = random.Random(semilla)
    n = rnd.randint(2, 7)
    inst = generar_instancia(20, 2, semilla=semilla)
    zona = rnd.sample(inst.clientes, n)
    tiempos = a_tiempos(matriz_aproximada(inst), inst.velocidad_kmh)
    origen = rnd.choice([0, zona[0].id])
    zona_sin = [c for c in zona if c.id != origen]
    t0 = inst.hora_salida + rnd.choice([0, 15, 40])
    esperado = fuerza_bruta_local(inst, zona_sin, tiempos, origen, t0)
    obtenido = llamar(m.ordenar_zona, zona_sin, inst, tiempos, origen, t0)
    if esperado is None:
        assert obtenido is None
    else:
        assert obtenido is not None
        assert obtenido[1] == pytest.approx(esperado[1])
        from ruta_optima.evaluador import evaluar_orden
        assert evaluar_orden(inst, obtenido[0], tiempos, origen, t0) == pytest.approx(esperado[1])
