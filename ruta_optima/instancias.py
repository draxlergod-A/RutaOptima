"""ROL 2 - Guardar/cargar instancias y crear instancias agrupadas por distritos.

Una "instancia" es un problema concreto: el almacén, los clientes y los parámetros.
Guardarla en un archivo JSON permite repetir EXACTAMENTE el mismo experimento.
"""

from __future__ import annotations

import json
import random
from dataclasses import asdict

from . import config
from .generador import generar_instancia
from .modelos import Cliente, Instancia


def guardar_instancia(inst: Instancia, ruta_archivo: str) -> None:
    """Guarda la instancia en un archivo JSON (asdict convierte las clases en diccionarios)."""
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        json.dump(asdict(inst), f, ensure_ascii=False, indent=1)


def cargar_instancia(ruta_archivo: str) -> Instancia:
    """Lee el JSON y reconstruye la Instancia (primero los Cliente, luego la Instancia)."""
    with open(ruta_archivo, encoding="utf-8") as f:
        datos = json.load(f)
    datos["deposito"] = Cliente(**datos["deposito"])
    datos["clientes"] = [Cliente(**c) for c in datos["clientes"]]
    return Instancia(**datos)


def generar_instancia_distritos(
    n: int, num_vehiculos: int | None = None, semilla: int = config.SEMILLA_DEFECTO
) -> Instancia:
    """Como `generar_instancia`, pero los clientes se agrupan alrededor de 4 a 6 "distritos".

    Se reutiliza la instancia aleatoria (demandas, ventanas, servicio) y solo se cambian las
    coordenadas: cada cliente se ubica cerca del centro de un distrito (distribución normal).
    """
    base = generar_instancia(n, num_vehiculos, semilla)
    azar = random.Random(semilla + 1000)
    area = config.AREA_KM
    centros = [(azar.uniform(2, area - 2), azar.uniform(2, area - 2))
               for _ in range(azar.randint(4, 6))]
    clientes = []
    for c in base.clientes:
        cx, cy = azar.choice(centros)
        x = min(area, max(0.0, azar.gauss(cx, 1.5)))   # recorta para no salirse del área
        y = min(area, max(0.0, azar.gauss(cy, 1.5)))
        clientes.append(Cliente(c.id, x, y, c.demanda, c.ventana_ini, c.ventana_fin, c.servicio))
    return Instancia(
        base.deposito, clientes, base.num_vehiculos, capacidad=base.capacidad,
        jornada_max=base.jornada_max, hora_salida=base.hora_salida,
        velocidad_kmh=base.velocidad_kmh, costo_km=base.costo_km,
        costo_hora=base.costo_hora, factor_vial=base.factor_vial, semilla=semilla,
    )


def instancias_de_prueba() -> dict[str, Instancia]:
    """Las 3 instancias fijas que usa todo el equipo para probar y medir."""
    return {
        "pequena": generar_instancia(8, 2, semilla=1),
        "mediana": generar_instancia(40, 4, semilla=2),
        "grande": generar_instancia(200, 15, semilla=3),
    }
