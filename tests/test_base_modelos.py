import pytest

from ruta_optima.generador import generar_instancia
from ruta_optima.modelos import Cliente, Instancia


def test_cliente_cero_es_el_almacen():
    inst = generar_instancia(5, 2, semilla=0)
    assert inst.cliente(0) is inst.deposito
    assert inst.cliente(3).id == 3
    assert inst.n == 5


def test_ids_deben_ser_consecutivos():
    deposito = Cliente(0, 0, 0, 0, 0, 1440, 0)
    malos = [Cliente(1, 0, 0, 1, 0, 100, 5), Cliente(3, 1, 1, 1, 0, 100, 5)]
    with pytest.raises(ValueError):
        Instancia(deposito, malos, 1)


def test_almacen_debe_tener_id_cero():
    with pytest.raises(ValueError):
        Instancia(Cliente(1, 0, 0, 0, 0, 1440, 0), [], 1)


def test_hora_limite():
    inst = generar_instancia(3, 1, semilla=0)
    assert inst.hora_limite == inst.hora_salida + inst.jornada_max
