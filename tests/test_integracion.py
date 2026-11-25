"""Prueba de punta a punta: solo corre cuando TODOS los módulos están listos."""
from ruta_optima.generador import generar_instancia
from ruta_optima.solver import comparar
from tests.ayudas import llamar


def test_ambas_estrategias_son_validas():
    inst = generar_instancia(40, 4, semilla=2)
    r = llamar(comparar, inst, 12)
    for nombre, (sol, ev) in r.items():
        assert ev.valida, (nombre, ev.errores)
        assert ev.atendidos + ev.no_atendidos == inst.n


def test_ambas_estrategias_validas_en_varias_semillas():
    for semilla in (1, 2, 3):
        inst = generar_instancia(60, semilla=semilla)
        for nombre, (sol, ev) in llamar(comparar, inst, 12).items():
            assert ev.valida, (semilla, nombre, ev.errores)


def test_instancia_grande_termina_rapido():
    import time
    inst = generar_instancia(200, semilla=3)
    t0 = time.perf_counter()
    llamar(comparar, inst, 12)
    assert time.perf_counter() - t0 < 60
