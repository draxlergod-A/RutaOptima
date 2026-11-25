"""ROL 8: corre todos los experimentos y guarda los CSV y gráficos en resultados/ (tarda ~1 minuto)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from ruta_optima.benchmark import ejecutar_benchmark

df = ejecutar_benchmark([20, 50, 100, 150, 200], [1, 2, 3, 4, 5], 12, "resultados")
resumen = df.groupby(["n", "estrategia"])[["costo_total", "distancia_km", "pct_atendidos", "tiempo_ejecucion_s"]].mean().round(2)
print(resumen.to_string())
print("Todas las soluciones válidas:", bool(df.valida.all()))

k_df = []
for k in (8, 10, 12, 14):
    d = ejecutar_benchmark([100], [1, 2, 3], k, None)
    d = d[d.estrategia == "dc_pd"].assign(k=k)
    k_df.append(d)
import pandas as pd
ek = pd.concat(k_df).groupby("k")[["costo_total", "pct_atendidos", "tiempo_ejecucion_s"]].mean().round(3)
ek.to_csv("resultados/experimento_k.csv")
print("\nEfecto de k (n = 100, estrategia dc_pd):"); print(ek.to_string())

with open("docs/RESULTADOS.md", "w", encoding="utf-8") as f:
    f.write("# Resultados del benchmark (promedio de 5 semillas)\n\n")
    f.write(resumen.reset_index().to_markdown(index=False) + "\n\n")
    f.write("## Efecto de k (n = 100)\n\n" + ek.reset_index().to_markdown(index=False) + "\n")
print("Guardado resultados/ y docs/RESULTADOS.md")
