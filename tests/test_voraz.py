"""ROL 5 - voraz.py"""
from ruta_optima import voraz as m
from ruta_optima.evaluador import evaluar
from ruta_optima.generador import generar_instancia
from ruta_optima.zonas import dividir_en_zonas
from tests.ayudas import instancia_manual, llamar, matriz_lineal


def test_asignar_zonas_respeta_capacidad_y_unicidad(inst_pequena, matrices_pequena):
    _, tiempos = matrices_pequena
    try:
        zonas = dividir_en_zonas(inst_pequena.clientes, 4)
    except NotImplementedError:
        zonas = [inst_pequena.clientes[:6], inst_pequena.clientes[6:]]
    por_vehiculo, sobrantes = llamar(m.asignar_zonas, zonas, inst_pequena, tiempos)
    assert len(por_vehiculo) <= inst_pequena.num_vehiculos
    vistos = [c.id for v in por_vehiculo for z in v for c in z] + [c.id for c in sobrantes]
    assert sorted(vistos) == sorted(c.id for c in inst_pequena.clientes)
    for v in por_vehiculo:
        assert sum(c.demanda for z in v for c in z) <= inst_pequena.capacidad


def test_ruta_voraz_es_valida(inst_pequena, matrices_pequena):
    dist, tiempos = matrices_pequena
    sol = llamar(m.ruta_voraz, inst_pequena, dist, tiempos)
    assert sol.nombre == "voraz"
    ev = evaluar(inst_pequena, sol, dist, tiempos)
    assert ev.valida, ev.errores


def test_ruta_voraz_con_capacidad_pequena():
    inst = generar_instancia(12, 6, semilla=2)
    inst = type(inst)(inst.deposito, inst.clientes, 6, capacidad=10)
    from ruta_optima.utilidades import a_tiempos, matriz_aproximada
    dist = matriz_aproximada(inst)
    tiempos = a_tiempos(dist, inst.velocidad_kmh)
    sol = llamar(m.ruta_voraz, inst, dist, tiempos)
    ev = evaluar(inst, sol, dist, tiempos)
    assert ev.valida, ev.errores


def test_cliente_imposible_va_a_no_atendidos():
    inst = instancia_manual([(540, 545), (540, 1000)])   # el 1 llega a las 550: imposible
    dist, tiempos = matriz_lineal(2)
    sol = llamar(m.ruta_voraz, inst, dist, tiempos)
    assert 1 in sol.no_atendidos
    assert evaluar(inst, sol, dist, tiempos).valida
