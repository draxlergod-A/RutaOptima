"""ROL 5 - Estrategias voraces: (1) vecino más cercano y (2) reparto de zonas a vehículos."""

from __future__ import annotations

from .evaluador import evaluar_orden
from .modelos import Cliente, Instancia, Solucion


def asignar_zonas(
    zonas: list[list[Cliente]],
    inst: Instancia,
    tiempos: list[list[float]],
) -> tuple[list[list[list[Cliente]]], list[Cliente]]:
    """Reparte zonas COMPLETAS entre los vehículos de forma equilibrada (regla voraz LPT).

    Se estima el trabajo de cada zona (servicio + viaje), se ordenan de mayor a menor y cada una
    se entrega al vehículo con MENOS trabajo acumulado que aún tenga capacidad.
    ¿Por qué no llenar un vehículo hasta su capacidad? Porque el límite real es el TIEMPO
    (jornada de 8 h y ventanas de 2 h): repartir el trabajo atiende a muchos más clientes.

    Devuelve (asignacion, sin_cupo): una lista de zonas por vehículo usado, y los clientes que
    no cupieron en ningún vehículo.
    """
    def demanda(z):
        return sum(c.demanda for c in z)

    def trabajo(z):   # minutos estimados: servicios + ida y vuelta + 6 min de viaje por cliente
        return sum(c.servicio for c in z) + 2 * min(tiempos[0][c.id] for c in z) + 6 * len(z)

    m = inst.num_vehiculos
    zonas_de = [[] for _ in range(m)]
    carga = [0] * m
    minutos = [0.0] * m
    sin_cupo: list[Cliente] = []

    for z in sorted(zonas, key=trabajo, reverse=True):
        con_cupo = [v for v in range(m) if carga[v] + demanda(z) <= inst.capacidad]
        if not con_cupo:
            sin_cupo.extend(z)
            continue
        v = min(con_cupo, key=lambda v: minutos[v])        # el vehículo menos ocupado
        zonas_de[v].append(z)
        carga[v] += demanda(z)
        minutos[v] += trabajo(z)

    asignacion = []
    for zs in (z for z in zonas_de if z):
        # Dentro de cada vehículo: primero la zona más cercana al almacén, luego la más
        # cercana a la anterior.
        pendientes, ordenadas = list(zs), []
        px, py = inst.deposito.x, inst.deposito.y
        while pendientes:
            z = min(pendientes,
                    key=lambda z: min((c.x - px) ** 2 + (c.y - py) ** 2 for c in z))
            pendientes.remove(z)
            ordenadas.append(z)
            px = sum(c.x for c in z) / len(z)
            py = sum(c.y for c in z) / len(z)
        asignacion.append(ordenadas)
    return asignacion, sin_cupo


def ruta_voraz(
    inst: Instancia,
    dist: list[list[float]],
    tiempos: list[list[float]],
) -> Solucion:
    """ESTRATEGIA 1: vecino más cercano, un vehículo a la vez, respetando todas las restricciones.

    El vehículo va siempre al cliente más cercano que todavía sea factible (cabe en la carga,
    llega dentro de su ventana y aún puede volver al almacén dentro de la jornada).
    """
    pendientes = {c.id: c for c in inst.clientes}
    rutas: list[list[int]] = []
    for _ in range(inst.num_vehiculos):
        if not pendientes:
            break
        ruta: list[int] = []
        posicion, carga = 0, 0
        while True:
            candidatos = sorted(
                (c for c in pendientes.values() if carga + c.demanda <= inst.capacidad),
                key=lambda c: dist[posicion][c.id],              # los más cercanos primero
            )
            for c in candidatos:
                if evaluar_orden(inst, ruta + [c.id], tiempos) is not None:   # ¿factible?
                    ruta.append(c.id)
                    carga += c.demanda
                    posicion = c.id
                    del pendientes[c.id]
                    break
            else:                                               # ningún candidato es factible
                break
        if ruta:
            rutas.append(ruta)
    return Solucion("voraz", rutas, sorted(pendientes))
