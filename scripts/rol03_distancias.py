"""ROL 3: prueba Dijkstra, mide cuánto tarda la matriz de distancias y compara con la línea recta."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import time
from ruta_optima.distancias import dijkstra, matriz_distancias
from ruta_optima.generador import generar_instancia
from ruta_optima.utilidades import matriz_aproximada

grafo = {0: [(1, 4.0), (2, 1.0)], 1: [(0, 4.0), (2, 2.0), (3, 5.0)], 2: [(0, 1.0), (1, 2.0)], 3: [(1, 5.0)]}
print("Dijkstra desde 0 (esperado {0: 0, 1: 3, 2: 1, 3: 8}):", dijkstra(grafo, 0))

lineas = ["n, segundos_matriz, km_promedio_calles, km_promedio_aproximado"]
for n in (20, 50, 100, 200):
    inst = generar_instancia(n, semilla=1)
    t0 = time.perf_counter(); d = matriz_distancias(inst); seg = time.perf_counter() - t0
    a = matriz_aproximada(inst)
    m = len(d); prom = lambda M: sum(map(sum, M)) / (m * m)
    print(f"n={n:3d}  matriz en {seg:.2f} s   km medio por calles={prom(d):.2f}   km medio línea recta x 1.3={prom(a):.2f}")
    lineas.append(f"{n}, {seg:.3f}, {prom(d):.3f}, {prom(a):.3f}")
open("resultados/rol03_distancias.csv", "w").write("\n".join(lineas) + "\n")
print("Guardado resultados/rol03_distancias.csv")
