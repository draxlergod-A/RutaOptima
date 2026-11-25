"""ROL 4: dibuja las zonas que crea divide y vencerás (resultados/zonas.png)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from ruta_optima.generador import generar_instancia
from ruta_optima.zonas import dividir_en_zonas

inst = generar_instancia(60, semilla=7)
for k in (12, 6):
    zonas = dividir_en_zonas(inst.clientes, k)
    print(f"k={k}: {len(zonas)} zonas, tamaños {[len(z) for z in zonas]}")
    fig, ax = plt.subplots(figsize=(6, 6))
    for i, z in enumerate(zonas):
        ax.scatter([c.x for c in z], [c.y for c in z], s=40, label=f"zona {i + 1} ({len(z)})", color=f"C{i % 10}")
    ax.scatter([inst.deposito.x], [inst.deposito.y], marker="s", s=100, c="black", label="almacén")
    ax.set_title(f"Divide y vencerás con k = {k}: {len(zonas)} zonas")
    ax.legend(fontsize=7, ncol=2); ax.set_aspect("equal"); fig.tight_layout()
    fig.savefig(f"resultados/zonas_k{k}.png", dpi=150); plt.close(fig)
print("Guardado resultados/zonas_k12.png y resultados/zonas_k6.png")
