"""ROL 4 - Divide y vencerás: partir a los clientes en zonas pequeñas con Quickselect."""

from __future__ import annotations

import random

from .modelos import Cliente


def quickselect(valores: list[float], k: int) -> float:
    """Devuelve el k-ésimo menor valor (k empieza en 0) sin ordenar todo. Promedio O(n).

    Idea: se elige un pivote y se separan los valores en menores / iguales / mayores;
    solo se continúa por el lado donde cae el índice k.
    """
    datos = list(valores)                      # copia: no se modifica la lista original
    azar = random.Random(0)                    # pivote "aleatorio" pero reproducible
    while True:
        pivote = datos[azar.randrange(len(datos))]
        menores = [x for x in datos if x < pivote]
        iguales = [x for x in datos if x == pivote]
        mayores = [x for x in datos if x > pivote]
        if k < len(menores):
            datos = menores
        elif k < len(menores) + len(iguales):
            return pivote
        else:
            k -= len(menores) + len(iguales)
            datos = mayores


def dividir_en_zonas(clientes: list[Cliente], k: int) -> list[list[Cliente]]:
    """Parte los clientes en zonas de a lo sumo `k` clientes.

    Divide: elige el eje (x o y) donde los clientes están más dispersos y corta por la MEDIANA,
    quedando dos mitades. Vence: repite en cada mitad hasta que tenga k clientes o menos.
    """
    if k < 1:
        raise ValueError("k debe ser al menos 1")
    if not clientes:
        return []
    if len(clientes) <= k:                     # caso base
        return [list(clientes)]

    xs = [c.x for c in clientes]
    ys = [c.y for c in clientes]
    usar_x = (max(xs) - min(xs)) >= (max(ys) - min(ys))
    eje = (lambda c: c.x) if usar_x else (lambda c: c.y)

    mitad = len(clientes) // 2
    mediana = quickselect([eje(c) for c in clientes], mitad)
    # Desempate por id: los que valen igual que la mediana se reparten hasta completar la mitad.
    menores = [c for c in clientes if eje(c) < mediana]
    iguales = sorted((c for c in clientes if eje(c) == mediana), key=lambda c: c.id)
    mayores = [c for c in clientes if eje(c) > mediana]
    faltan = mitad - len(menores)
    izquierda = menores + iguales[:faltan]
    derecha = iguales[faltan:] + mayores
    return dividir_en_zonas(izquierda, k) + dividir_en_zonas(derecha, k)
