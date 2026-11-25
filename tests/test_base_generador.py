import pytest

from ruta_optima import config
from ruta_optima.generador import generar_instancia, vehiculos_por_defecto


def test_misma_semilla_misma_instancia():
    assert generar_instancia(30, 3, semilla=5) == generar_instancia(30, 3, semilla=5)


def test_distinta_semilla_distinta_instancia():
    assert generar_instancia(30, 3, semilla=5) != generar_instancia(30, 3, semilla=6)


def test_rangos_de_la_tabla_1():
    inst = generar_instancia(200, semilla=3)
    assert inst.n == 200
    for c in inst.clientes:
        assert config.DEMANDA_RANGO[0] <= c.demanda <= config.DEMANDA_RANGO[1]
        assert config.SERVICIO_RANGO_MIN[0] <= c.servicio <= config.SERVICIO_RANGO_MIN[1]
        assert c.ventana_fin - c.ventana_ini == config.VENTANA_DURACION_MIN
        assert config.VENTANA_INICIO_MIN <= c.ventana_ini <= config.VENTANA_INICIO_MAX
        assert (c.ventana_ini - config.VENTANA_INICIO_MIN) % config.VENTANA_PASO_MIN == 0
        assert 0 <= c.x <= config.AREA_KM and 0 <= c.y <= config.AREA_KM


def test_vehiculos_por_defecto_dentro_de_la_flota():
    for n in (1, 20, 100, 200, 500):
        assert 2 <= vehiculos_por_defecto(n) <= config.FLOTA_MAX


def test_n_invalido():
    with pytest.raises(ValueError):
        generar_instancia(0)
