"""ROL 6: mide cuánto tarda Held-Karp según k, el tamaño de la zona (resultados/held_karp_tiempo.png)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from ruta_optima.config import VENTANA_DURACION_MIN
from ruta_optima.generador import generar_instancia
from ruta_optima.held_karp import ordenar_zona
from ruta_optima.modelos import Cliente, Instancia
from ruta_optima.utilidades import a_tiempos, matriz_aproximada

# Peor caso: ventanas anchas (todo es factible), así Held-Karp no puede descartar estados.
base = generar_instancia(16, 2, semilla=1)
anchos = [Cliente(c.id, c.x, c.y, c.demanda, 540, 1100, c.servicio) for c in base.clientes]
inst = Instancia(base.deposito, anchos, 2, jornada_max=1000)
tiempos = a_tiempos(matriz_aproximada(inst), inst.velocidad_kmh)
ks, ts = [], []
for k in range(4, 15):
    t0 = time.perf_counter(); res = ordenar_zona(inst.clientes[:k], inst, tiempos); seg = time.perf_counter() - t0
    ks.append(k); ts.append(seg)
    print(f"k={k:2d}  {seg:8.3f} s  orden encontrado: {res is not None}")
fig, ax = plt.subplots(figsize=(6, 4))
ax.semilogy(ks, ts, marker="o"); ax.set_xlabel("k (clientes en la zona)"); ax.set_ylabel("segundos (escala log)")
ax.set_title("Held-Karp: crece como 2^k"); ax.grid(alpha=.3); fig.tight_layout()
fig.savefig("resultados/held_karp_tiempo.png", dpi=150)
print("Guardado resultados/held_karp_tiempo.png")
