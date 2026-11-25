"""Punto de entrada del proyecto.

Uso:
    python main.py                      -> muestra el estado y, si todo está listo, compara las estrategias
    python main.py --estado             -> solo muestra qué módulos faltan
    python main.py --n 60 --vehiculos 5 --semilla 7
"""

from __future__ import annotations

import argparse
import sys

from ruta_optima import config
from ruta_optima.estado import imprimir_estado
from ruta_optima.generador import generar_instancia
from ruta_optima.solver import comparar


def main() -> int:
    ap = argparse.ArgumentParser(description="Optimización de rutas de reparto de última milla")
    ap.add_argument("--estado", action="store_true", help="solo mostrar el estado de los módulos")
    ap.add_argument("--n", type=int, default=30, help="número de clientes (por defecto 30)")
    ap.add_argument("--vehiculos", type=int, default=None, help="número de vehículos")
    ap.add_argument("--semilla", type=int, default=config.SEMILLA_DEFECTO)
    ap.add_argument("--k", type=int, default=config.K_ZONA, help="máximo de clientes por zona")
    args = ap.parse_args()

    faltan = imprimir_estado()
    if args.estado:
        return 0
    if faltan:
        print("Aún faltan módulos: cuando terminen, este comando comparará las dos estrategias.")
        print("Mira docs/tareas/ para saber qué le toca a cada rol.\n")
        return 0

    inst = generar_instancia(args.n, args.vehiculos, args.semilla)
    print(f"Instancia: {inst.n} clientes, {inst.num_vehiculos} vehículos, semilla {inst.semilla}")
    resultados = comparar(inst, args.k)

    print(f"\n{'estrategia':<10} {'valida':<7} {'costo S/':>10} {'km':>8} {'horas':>7} "
          f"{'veh.':>5} {'atend.%':>8} {'seg':>8}")
    for nombre, (sol, ev) in resultados.items():
        print(f"{nombre:<10} {str(ev.valida):<7} {ev.costo_total:>10.2f} {ev.distancia_km:>8.1f} "
              f"{ev.horas_operacion:>7.1f} {ev.vehiculos_usados:>5} {ev.pct_atendidos:>8.1f} "
              f"{sol.tiempo_ejecucion_s:>8.3f}")
        for e in ev.errores[:3]:
            print(f"   ! {e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
