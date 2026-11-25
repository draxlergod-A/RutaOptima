"""ROL 8 - benchmark.py"""
from ruta_optima import benchmark as m
from tests.ayudas import llamar


def test_benchmark_columnas_y_filas():
    df = llamar(m.ejecutar_benchmark, [10, 14], [1], 8, None)
    assert list(df.columns) == m.COLUMNAS
    assert len(df) == 4                       # 2 tamaños x 1 semilla x 2 estrategias
    assert set(df["estrategia"]) == {"voraz", "dc_pd"}
    assert df["valida"].all()


def test_graficar_crea_archivos(tmp_path):
    df = llamar(m.ejecutar_benchmark, [10, 14], [1], 8, None)
    m.graficar(df, str(tmp_path))
    for f in ("tiempo_vs_n.png", "costo_vs_n.png", "atendidos_vs_n.png"):
        assert (tmp_path / f).exists()
