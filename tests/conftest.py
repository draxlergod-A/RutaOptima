"""Configuración compartida de las pruebas (pytest la carga sola)."""

import pytest

from ruta_optima.generador import generar_instancia
from ruta_optima.utilidades import a_tiempos, matriz_aproximada


@pytest.fixture
def inst_pequena():
    """12 clientes, 2 vehículos."""
    return generar_instancia(12, 2, semilla=1)


@pytest.fixture
def matrices_pequena(inst_pequena):
    """(dist, tiempos) APROXIMADAS, para probar sin depender del ROL 3."""
    dist = matriz_aproximada(inst_pequena)
    return dist, a_tiempos(dist, inst_pequena.velocidad_kmh)
