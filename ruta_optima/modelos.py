"""Estructuras de datos del proyecto (el "contrato" que usan todos los módulos).

Convenciones (leer antes de programar tu parte):
  * El almacén (depósito) tiene id = 0. Los clientes tienen id = 1, 2, ..., n.
  * Las matrices de distancia y tiempo se indexan con el id: matriz[i][j].
    Por eso miden (n + 1) x (n + 1).
  * Una ruta es una lista de ids de clientes en el orden de visita. NO incluye
    el almacén: se asume que sale del almacén y regresa al almacén.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from . import config


@dataclass(frozen=True)
class Cliente:
    """Un cliente (o el almacén, que es el cliente 0)."""

    id: int
    x: float            # km
    y: float            # km
    demanda: int        # paquetes
    ventana_ini: float  # minutos desde 00:00: no se puede empezar a servir antes
    ventana_fin: float  # minutos desde 00:00: no se puede empezar a servir después
    servicio: float     # minutos que toma entregar el pedido


@dataclass
class Instancia:
    """Un día de reparto: almacén, clientes, flota y parámetros."""

    deposito: Cliente
    clientes: list[Cliente]
    num_vehiculos: int
    capacidad: int = config.CAPACIDAD
    jornada_max: float = config.JORNADA_MAX_MIN
    hora_salida: float = config.HORA_SALIDA_MIN
    velocidad_kmh: float = config.VELOCIDAD_KMH
    costo_km: float = config.COSTO_KM
    costo_hora: float = config.COSTO_HORA
    factor_vial: float = config.FACTOR_VIAL
    semilla: int = 0

    def __post_init__(self) -> None:
        if self.deposito.id != 0:
            raise ValueError("El almacén debe tener id = 0")
        for pos, c in enumerate(self.clientes, start=1):
            if c.id != pos:
                raise ValueError(
                    f"Los clientes deben tener ids 1..n en orden (posición {pos} tiene id {c.id})"
                )
        if self.num_vehiculos < 1:
            raise ValueError("Debe haber al menos 1 vehículo")

    @property
    def n(self) -> int:
        """Número de clientes (sin contar el almacén)."""
        return len(self.clientes)

    @property
    def demanda_total(self) -> int:
        return sum(c.demanda for c in self.clientes)

    @property
    def hora_limite(self) -> float:
        """Instante máximo en que un vehículo puede estar de vuelta en el almacén."""
        return self.hora_salida + self.jornada_max

    def cliente(self, id_: int) -> Cliente:
        """Devuelve el cliente con ese id (0 = almacén)."""
        if id_ == 0:
            return self.deposito
        return self.clientes[id_ - 1]


@dataclass
class Solucion:
    """Resultado de una estrategia: las rutas y los clientes que no se pudieron atender."""

    nombre: str
    rutas: list[list[int]] = field(default_factory=list)   # una lista de ids por vehículo
    no_atendidos: list[int] = field(default_factory=list)  # ids de clientes sin ruta
    tiempo_ejecucion_s: float = 0.0                         # lo llena solver.py
