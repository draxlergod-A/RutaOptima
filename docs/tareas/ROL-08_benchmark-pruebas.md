# ROL 8: Experimentos, gráficos y casos extremos

Corre las dos estrategias con 20 a 200 clientes y 5 semillas, y guarda tablas y gráficos para el informe.

> **El código ya está terminado y probado.** Tu tarea es corta: ejecutar, entender tu parte, guardar la evidencia y poder explicarla.

| | |
|---|---|
| **Tu rama** | `feature/rol08-benchmark-pruebas` |
| **Tu parte en el código** | `ruta_optima/benchmark.py y tests/test_casos_borde.py` |
| **Tiempo estimado** | 30–45 minutos |

## Paso 1. Preparar (una sola vez)
```bash
git clone <URL-DEL-REPOSITORIO>
cd ruta-optima-ultima-milla
git checkout feature/rol08-benchmark-pruebas
python -m pip install -r requirements.txt
```
Si Git dice que la rama no existe, créala: `git checkout -b feature/rol08-benchmark-pruebas`.

## Paso 2. Ejecutar
```bash
python scripts/rol08_benchmark.py
```
Debe terminar sin errores y mostrar resultados en la terminal. Si falla, mira `EJECUTAR.md` (sección «Si algo falla»).

## Paso 3. Qué debes guardar (entrega)
- `resultados/resultados.csv`
- `resultados/*.png`
- `resultados/experimento_k.csv`
- `docs/RESULTADOS.md`
- `tests/test_casos_borde.py (2 pruebas nuevas)`

## Pruebas nuevas (pegar tal cual)
Abre `tests/test_casos_borde.py`. **Borra** las dos pruebas marcadas con `@pytest.mark.skip` (`test_capacidad_insuficiente` y `test_ventanas_imposibles`) y pega al final del archivo:

```python
def test_capacidad_insuficiente():
    from ruta_optima.modelos import Instancia
    base = generar_instancia(20, 2, semilla=1)
    inst = Instancia(base.deposito, base.clientes, 2, capacidad=10)   # capacidad total 20 < demanda
    for nombre, (sol, ev) in comparar(inst, 12).items():
        assert ev.valida, (nombre, ev.errores)
        assert ev.no_atendidos > 0


def test_ventanas_imposibles():
    from dataclasses import replace
    from ruta_optima.modelos import Instancia
    base = generar_instancia(10, 3, semilla=1)
    clientes = [replace(c, ventana_ini=0.0, ventana_fin=1.0) for c in base.clientes]  # cierran a las 00:01
    inst = Instancia(base.deposito, clientes, 3)
    for nombre, (sol, ev) in comparar(inst, 12).items():
        assert ev.valida, (nombre, ev.errores)
        assert ev.atendidos == 0
```
Corre `python -m pytest tests/test_casos_borde.py -v`: deben pasar las 5 pruebas y ya no debe haber SKIPPED.


## Paso 4. Entiende tu parte (te la van a preguntar)
Abre el archivo indicado, lee los comentarios y responde estas preguntas **con tus palabras** en la sección «Mis respuestas» de más abajo.

1. **¿Qué estrategia tiene menor costo y cuál atiende más clientes? ¿Cambia con n?**  
   _Dónde mirar:_ Mira la tabla que imprime el script y `docs/RESULTADOS.md`.
2. **¿Qué efecto tiene k (tamaño de zona) en costo y tiempo?**  
   _Dónde mirar:_ `resultados/experimento_k.csv`.
3. **¿Por qué se usan 5 semillas y se promedia?**  
   _Dónde mirar:_ Una sola instancia puede ser casual; el promedio es más confiable.

Tu guion de 1 minuto para la exposición está en `docs/PRESENTACION.md` (busca tu rol).

## Mis respuestas
_(Escribe aquí tus respuestas, 2 o 3 líneas por pregunta.)_

1. Depende de n. **Divide y vencerás + PD** tiene menor costo con 20, 50 y 100 clientes (por ejemplo, S/ 993.90 vs S/ 1117.95 con 50), y atiende más clientes con 20, 50, 150 y 200. Con 100 clientes el voraz atiende un poco más (97.8 % vs 95.0 %). Con 150 y 200 el voraz sale más barato, pero porque atiende a menos clientes (77.3 % vs 90.9 % con 150). El voraz siempre es el más rápido (milisegundos).
2. Con k = 8 y k = 10 el costo es igual (S/ 2120.00) y tarda unos 0.002 s. Con k = 12 baja a S/ 1840.83 (0.06 s) y con k = 14 baja a S/ 1495.57, pero tarda 0.16 s. Es decir, zonas más grandes dan rutas más baratas porque Held-Karp optimiza más clientes juntos, pero el tiempo crece muy rápido (O(k²·2^k)). Por eso usamos k = 12 como punto medio.
3. Porque una sola instancia puede salir "con suerte" o "sin suerte" para una estrategia (clientes muy juntos o muy dispersos). Con 5 semillas distintas probamos 5 problemas diferentes de cada tamaño y promediamos, así el resultado es más confiable y la comparación es justa. Además, cada semilla es reproducible: cualquiera puede repetir el experimento y obtener los mismos números.

## Paso 5. Subir tu trabajo (rama → Pull Request → main)
```bash
git add .
git commit -m "docs(rol08): evidencia y respuestas"
git push -u origin feature/rol08-benchmark-pruebas
```
En GitHub: **Compare & pull request** hacia `main` → completa la plantilla → pide revisión a un compañero → cuando las pruebas (Actions) estén en verde, **Merge pull request**.
Antes de abrir el PR, cambia en el `README.md` **solo tu fila** del tablero: pon tu nombre y ✅. Guía de Git: `docs/GUIA_GIT.md`.

## Lista de verificación
- [x] Ejecuté el comando del Paso 2 sin errores
- [x] Guardé los archivos de entrega
- [x] Escribí mis respuestas
- [x] Actualicé mi fila del README
- [x] Abrí el Pull Request y se unió a `main`
