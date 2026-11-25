"""ROL 8 - Experimentos: corre las dos estrategias en varios tamaños y arma tablas y gráficos."""

from __future__ import annotations

import os

import matplotlib

matplotlib.use("Agg")          # dibuja sin abrir ventanas
import matplotlib.pyplot as plt
import pandas as pd

from . import config
from .generador import generar_instancia
from .solver import comparar

COLUMNAS = [
    "n", "semilla", "estrategia", "costo_total", "distancia_km", "horas_operacion",
    "vehiculos_usados", "atendidos", "no_atendidos", "pct_atendidos",
    "tiempo_ejecucion_s", "valida",
]


def ejecutar_benchmark(
    tamanos: list[int],
    semillas: list[int],
    k: int = config.K_ZONA,
    carpeta: str | None = "resultados",
    num_vehiculos: int | None = None,
) -> pd.DataFrame:
    """Una fila por (tamaño, semilla, estrategia). Si `carpeta` no es None guarda CSV y gráficos."""
    filas = []
    for n in tamanos:
        for semilla in semillas:
            inst = generar_instancia(n, num_vehiculos, semilla)
            for nombre, (sol, ev) in comparar(inst, k).items():
                filas.append({
                    "n": n, "semilla": semilla, "estrategia": nombre,
                    "costo_total": ev.costo_total, "distancia_km": ev.distancia_km,
                    "horas_operacion": ev.horas_operacion, "vehiculos_usados": ev.vehiculos_usados,
                    "atendidos": ev.atendidos, "no_atendidos": ev.no_atendidos,
                    "pct_atendidos": ev.pct_atendidos,
                    "tiempo_ejecucion_s": sol.tiempo_ejecucion_s, "valida": ev.valida,
                })
    df = pd.DataFrame(filas, columns=COLUMNAS)
    if carpeta:
        os.makedirs(carpeta, exist_ok=True)
        df.to_csv(os.path.join(carpeta, "resultados.csv"), index=False)
        graficar(df, carpeta)
    return df


def graficar(df: pd.DataFrame, carpeta: str) -> list[str]:
    """Tres gráficos (promedio por tamaño): tiempo, costo y % atendidos, una línea por estrategia."""
    os.makedirs(carpeta, exist_ok=True)
    etiquetas = {"voraz": "Voraz", "dc_pd": "Divide y vencerás + PD"}
    graficos = [
        ("tiempo_ejecucion_s", "Tiempo de ejecución (s)", "tiempo_vs_n.png"),
        ("costo_total", "Costo total (S/)", "costo_vs_n.png"),
        ("pct_atendidos", "Clientes atendidos (%)", "atendidos_vs_n.png"),
    ]
    archivos = []
    for columna, titulo, nombre in graficos:
        fig, ax = plt.subplots(figsize=(6, 4))
        for estrategia, grupo in df.groupby("estrategia"):
            promedio = grupo.groupby("n")[columna].mean()
            ax.plot(promedio.index, promedio.values, marker="o",
                    label=etiquetas.get(estrategia, estrategia))
        ax.set_xlabel("Número de clientes (n)")
        ax.set_ylabel(titulo)
        ax.set_title(titulo + " vs. n")
        ax.grid(alpha=0.3)
        ax.legend()
        fig.tight_layout()
        ruta = os.path.join(carpeta, nombre)
        fig.savefig(ruta, dpi=150)
        plt.close(fig)
        archivos.append(ruta)
    return archivos
