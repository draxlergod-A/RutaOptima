"""Pruebas del evaluador (ROL 1). Usan una línea de puntos: el cliente i está a i*10 minutos."""

import pytest

from ruta_optima.evaluador import evaluar, evaluar_orden, simular_ruta
from ruta_optima.modelos import Solucion
from tests.ayudas import instancia_manual, matriz_lineal

ANCHA = (540, 1000)


def test_evaluar_orden_espera_si_llega_antes_de_la_ventana():
    inst = instancia_manual([(600, 720), (540, 560)])
    _, tiempos = matriz_lineal(2)
    # Visita 2 (llega 560, justo en su límite) y luego 1 (llega 575, espera hasta 600)
    assert evaluar_orden(inst, [2, 1], tiempos) == pytest.approx(605)
    # Visita 1 primero: termina 605 y llegaría tarde al cliente 2
    assert evaluar_orden(inst, [1, 2], tiempos) is None


def test_evaluar_orden_vacio():
    inst = instancia_manual([ANCHA])
    _, tiempos = matriz_lineal(1)
    assert evaluar_orden(inst, [], tiempos) == 540
    assert evaluar_orden(inst, [], tiempos, t_inicio=600) == 600


def test_evaluar_orden_desde_otro_origen():
    inst = instancia_manual([ANCHA, ANCHA])
    _, tiempos = matriz_lineal(2)
    # Parte del cliente 1 a las 10:00 hacia el cliente 2: 600 + 10 + 5 de servicio
    assert evaluar_orden(inst, [2], tiempos, origen=1, t_inicio=600) == pytest.approx(615)


def test_evaluar_orden_respeta_la_jornada():
    # Atiende en 555 y necesita 10 min para volver: llega a 565
    assert evaluar_orden(instancia_manual([(540, 600)], jornada=30), [1], matriz_lineal(1)[1]) \
        == pytest.approx(555)
    assert evaluar_orden(instancia_manual([(540, 600)], jornada=20), [1], matriz_lineal(1)[1]) is None


def test_evaluar_orden_ventana_imposible():
    inst = instancia_manual([(540, 545)])  # llegaría a las 550
    assert evaluar_orden(inst, [1], matriz_lineal(1)[1]) is None


def test_simular_ruta_calcula_distancia_y_duracion():
    inst = instancia_manual([ANCHA, ANCHA])
    dist, tiempos = matriz_lineal(2)
    r = simular_ruta(inst, [1, 2], dist, tiempos)
    assert r.factible
    assert r.distancia_km == pytest.approx(8.0)       # 2 + 2 + 4
    assert r.duracion_min == pytest.approx(50.0)      # 10+5 + 10+5 + 20
    assert r.carga == 2


def test_evaluar_costo():
    inst = instancia_manual([ANCHA, ANCHA])
    dist, tiempos = matriz_lineal(2)
    ev = evaluar(inst, Solucion("x", [[1, 2]], []), dist, tiempos)
    assert ev.valida
    assert ev.costo_total == pytest.approx(1.2 * 8.0 + 12.5 * (50 / 60))
    assert ev.vehiculos_usados == 1 and ev.pct_atendidos == 100.0


def test_evaluar_detecta_llegada_tarde():
    inst = instancia_manual([(540, 545)])
    dist, tiempos = matriz_lineal(1)
    ev = evaluar(inst, Solucion("x", [[1]], []), dist, tiempos)
    assert not ev.valida and any("ventana" in e for e in ev.errores)


def test_evaluar_detecta_capacidad():
    inst = instancia_manual([ANCHA, ANCHA], demandas=[60, 60])
    dist, tiempos = matriz_lineal(2)
    ev = evaluar(inst, Solucion("x", [[1, 2]], []), dist, tiempos)
    assert not ev.valida and any("capacidad" in e for e in ev.errores)


def test_evaluar_detecta_cliente_repetido_y_faltante():
    inst = instancia_manual([ANCHA, ANCHA, ANCHA], num_vehiculos=2)
    dist, tiempos = matriz_lineal(3)
    repetido = evaluar(inst, Solucion("x", [[1, 2], [2, 3]], []), dist, tiempos)
    assert not repetido.valida and any("2 veces" in e for e in repetido.errores)
    faltante = evaluar(inst, Solucion("x", [[1, 2]], []), dist, tiempos)
    assert not faltante.valida and any("ninguna ruta" in e for e in faltante.errores)


def test_evaluar_detecta_demasiados_vehiculos():
    inst = instancia_manual([ANCHA, ANCHA], num_vehiculos=1)
    dist, tiempos = matriz_lineal(2)
    ev = evaluar(inst, Solucion("x", [[1], [2]], []), dist, tiempos)
    assert not ev.valida and any("vehículos" in e for e in ev.errores)


def test_no_atendidos_cuentan_como_cubiertos():
    inst = instancia_manual([ANCHA, ANCHA])
    dist, tiempos = matriz_lineal(2)
    ev = evaluar(inst, Solucion("x", [[1]], [2]), dist, tiempos)
    assert ev.valida and ev.no_atendidos == 1 and ev.pct_atendidos == 50.0
