"""ROL 5: ¿cuántos clientes atiende cada estrategia según la cantidad de vehículos? (resultados/atendidos_vs_vehiculos.png)"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from ruta_optima.generador import generar_instancia
from ruta_optima.solver import comparar

flota = [2, 4, 6, 8, 10, 12, 15]
y = {"voraz": [], "dc_pd": []}
for m in flota:
    prom = {"voraz": 0.0, "dc_pd": 0.0}
    for semilla in (1, 2, 3):
        for nombre, (_, ev) in comparar(generar_instancia(100, m, semilla), 12).items():
            prom[nombre] += ev.pct_atendidos / 3
    for nombre in y: y[nombre].append(prom[nombre])
    print(f"vehículos={m:2d}  voraz={prom['voraz']:.1f} %  dc_pd={prom['dc_pd']:.1f} %")
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(flota, y["voraz"], marker="o", label="Voraz"); ax.plot(flota, y["dc_pd"], marker="o", label="Divide y vencerás + PD")
ax.set_xlabel("Vehículos"); ax.set_ylabel("% atendidos (n = 100)"); ax.grid(alpha=.3); ax.legend(); fig.tight_layout()
fig.savefig("resultados/atendidos_vs_vehiculos.png", dpi=150)
print("Guardado resultados/atendidos_vs_vehiculos.png")
