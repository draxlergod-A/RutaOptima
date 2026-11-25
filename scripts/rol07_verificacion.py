"""ROL 7: verifica que Held-Karp da el MISMO óptimo que la fuerza bruta y compara sus tiempos."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import random, time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from ruta_optima.fuerza_bruta import mejor_orden_fuerza_bruta
from ruta_optima.generador import generar_instancia
from ruta_optima.held_karp import ordenar_zona
from ruta_optima.utilidades import a_tiempos, matriz_aproximada

azar = random.Random(0)
iguales = total = 0
for semilla in range(200):
    inst = generar_instancia(20, 3, semilla=semilla)
    tiempos = a_tiempos(matriz_aproximada(inst), inst.velocidad_kmh)
    zona = azar.sample(inst.clientes, azar.randint(2, 7))
    a, b = ordenar_zona(zona, inst, tiempos), mejor_orden_fuerza_bruta(zona, inst, tiempos)
    total += 1
    iguales += (a is None and b is None) or (a is not None and b is not None and abs(a[1] - b[1]) < 1e-6)
print(f"Held-Karp y fuerza bruta coinciden en {iguales} de {total} zonas al azar")

inst = generar_instancia(12, 2, semilla=1)
from ruta_optima.modelos import Cliente, Instancia
anchos = [Cliente(c.id, c.x, c.y, c.demanda, 540, 1100, c.servicio) for c in inst.clientes]
inst = Instancia(inst.deposito, anchos, 2, jornada_max=1000)
tiempos = a_tiempos(matriz_aproximada(inst), inst.velocidad_kmh)
ks, tb, th = [], [], []
for k in range(4, 10):
    z = inst.clientes[:k]
    t0 = time.perf_counter(); mejor_orden_fuerza_bruta(z, inst, tiempos); tb.append(time.perf_counter() - t0)
    t0 = time.perf_counter(); ordenar_zona(z, inst, tiempos); th.append(time.perf_counter() - t0); ks.append(k)
    print(f"k={k}  fuerza bruta {tb[-1]:.4f} s   Held-Karp {th[-1]:.4f} s")
fig, ax = plt.subplots(figsize=(6, 4))
ax.semilogy(ks, tb, marker="o", label="Fuerza bruta  O(k!)"); ax.semilogy(ks, th, marker="o", label="Held-Karp  O(k²·2^k)")
ax.set_xlabel("k"); ax.set_ylabel("segundos (log)"); ax.grid(alpha=.3); ax.legend(); fig.tight_layout()
fig.savefig("resultados/fuerza_bruta_vs_held_karp.png", dpi=150)
print("Guardado resultados/fuerza_bruta_vs_held_karp.png")
