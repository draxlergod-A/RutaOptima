# Cómo ejecutar el proyecto (5 minutos)

## 1. Requisito: Python 3.10 o más nuevo
Revisa con `python --version`. Si no lo tienes: https://www.python.org/downloads/ (en Windows marca **Add Python to PATH**).

## 2. Instalar (una sola vez)
Abre una terminal **dentro de la carpeta del proyecto** y escribe:
```
python -m pip install -r requirements.txt
```

## 3. Abrir la página web
```
python app.py
```
Se abre sola en el navegador: **http://localhost:8000**. (Si no se abre, copia esa dirección en el navegador.)
Para detenerla: `Ctrl + C` en la terminal.

> En Windows también puedes hacer **doble clic en `ejecutar.bat`** (instala y abre la página).

### Qué puedes hacer en la página
- Mover los controles (clientes, vehículos, k, semilla) y presionar **Calcular rutas**.
- Ver la **comparación** (costo, km, horas, % atendidos, tiempo) y los **mapas** de las dos estrategias.
- Marcar «Mostrar las zonas» para ver cómo divide y vencerás parte la ciudad.
- Pestaña **Detalle de rutas**: hora de llegada, espera y ventana de cada cliente.
- Pestaña **Experimentos**: gráficos del benchmark.

## 4. Otras formas de ejecutar
| Qué | Comando |
|---|---|
| Comparar en la consola | `python main.py --n 60 --vehiculos 9` |
| Ver qué módulos están listos | `python main.py --estado` |
| Correr todas las pruebas | `python -m pytest` |
| Rehacer los experimentos y gráficos | `python scripts/rol08_benchmark.py` |

## Si algo falla
- `python no se reconoce`: reinstala Python marcando *Add Python to PATH*; o prueba `py` en vez de `python`.
- `No module named ...`: repite el paso 2.
- «Address already in use»: cierra la otra terminal con la página, o usa otro puerto: `python app.py --puerto 8010`.
