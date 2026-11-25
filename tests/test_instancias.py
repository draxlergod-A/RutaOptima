"""ROL 2 - instancias.py"""
from ruta_optima import instancias as m
from ruta_optima.generador import generar_instancia
from tests.ayudas import llamar


def test_guardar_y_cargar_es_identico(tmp_path):
    inst = generar_instancia(25, 3, semilla=9)
    ruta = tmp_path / "inst.json"
    llamar(m.guardar_instancia, inst, str(ruta))
    assert m.cargar_instancia(str(ruta)) == inst


def test_tres_instancias_de_prueba():
    d = llamar(m.instancias_de_prueba)
    assert set(d) == {"pequena", "mediana", "grande"}
    assert (d["pequena"].n, d["mediana"].n, d["grande"].n) == (8, 40, 200)
    assert d["grande"].num_vehiculos == 15


def test_instancia_por_distritos():
    inst = llamar(m.generar_instancia_distritos, 60, 4, 1)
    assert inst.n == 60 and inst.num_vehiculos == 4
    assert all(0 <= c.x <= 20 and 0 <= c.y <= 20 for c in inst.clientes)
