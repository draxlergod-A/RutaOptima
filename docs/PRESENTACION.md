# Guía para grabar el video de la exposición (≈ 20 minutos)

El video se graba en **Google Meet** con todo el equipo. Cada integrante expone su parte siguiendo **siempre el mismo orden**:

1. **Muestra el código y explica qué hace** (archivo y líneas exactas, más abajo).
2. **Lo ejecuta** en la terminal y explica lo que sale en pantalla.
3. **Pasa la palabra** al siguiente con la frase de su guion.

No hace falta memorizar: lee tu guion una o dos veces y **dilo con tus palabras**. Todos los comandos y resultados de esta guía se probaron sobre la versión final de `main`; en tu PC los **tiempos en segundos** pueden variar un poco, pero los costos y porcentajes salen iguales.

---

## 1. Cómo grabamos

- **Luis Angel** abre la reunión de Meet y presiona **Grabar** (Actividades → Grabación). Al final la detiene y el video queda en su Google Drive.
- **Cámara encendida** todos; micrófono en silencio cuando no te toca hablar.
- **Cuando te toque, compartes TU pantalla** (botón «Presentar ahora» → «Toda la pantalla»), con **VS Code** abierto en tu archivo y una **terminal** dentro de VS Code (menú *Terminal → Nueva terminal*).
- **Plan B:** si a alguien no le funciona el proyecto o no puede compartir, **Luis Angel comparte su pantalla**, abre el archivo y ejecuta el comando mientras esa persona habla.
- Si te equivocas, no pasa nada: respira, repite la frase y sigue. Es mejor eso que cortar el video.

## 2. Preparación de cada integrante (el día anterior, 10 minutos)

1. Traer la última versión del proyecto. Si **ya tienes** la carpeta:
   ```bash
   git checkout main
   git pull origin main
   ```
   Si **no la tienes**: `git clone https://github.com/draxlergod-A/RutaOptima.git` y luego `cd RutaOptima`.
2. Instalar lo necesario (una sola vez):
   ```bash
   python -m pip install -r requirements.txt
   ```
3. Abrir la carpeta en VS Code (*Archivo → Abrir carpeta*).
4. **Ejecutar una vez tu comando** (está en tu sección) y comprobar que sale lo mismo que dice esta guía.
5. Dejar abierto tu archivo en la línea que vas a explicar, y la imagen de `resultados/` que vas a mostrar.

> Si `python` no se reconoce en Windows, usa `py` en lugar de `python` (por ejemplo, `py scripts/rol03_distancias.py`).
> Al ejecutar los scripts se vuelven a crear los archivos de `resultados/`. Es normal: **no hagan `git push` después de grabar**.

## 3. Orden, tiempos y qué muestra cada uno

| # | Rol | Quién | Tiempo | Código que explica | Comando que ejecuta |
|---|---|---|---|---|---|
| 1 | ROL 1 · Problema y proyecto | Luis Angel López Siccha | 2.5 min | `ruta_optima/solver.py` y `evaluador.py` | `python main.py --n 60` y `python -m pytest` |
| 2 | ROL 2 · Instancias | Edgar Ismael Victorio Capa | 1.5 min | `ruta_optima/generador.py` y `instancias.py` | `python scripts/rol02_instancias.py` |
| 3 | ROL 3 · Distancias (Dijkstra) | Luis Fernando Reyes Casiano | 2 min | `ruta_optima/distancias.py` | `python scripts/rol03_distancias.py` |
| 4 | ROL 4 · Zonas (divide y vencerás) | Cristofher Maguiña Peche | 2 min | `ruta_optima/zonas.py` | `python scripts/rol04_zonas.py` |
| 5 | ROL 5 · Voraz | Carlo Stefano Soel Olivo | 2 min | `ruta_optima/voraz.py` | `python scripts/rol05_voraz.py` |
| 6 | ROL 6 · Programación dinámica | Aldrin Juaquin Meliton Espinoza | 2 min | `ruta_optima/held_karp.py` | `python scripts/rol06_held_karp.py` |
| 7 | ROL 7 · Fuerza bruta | Fredy Abraham Núñez Cerdán | 1.5 min | `ruta_optima/fuerza_bruta.py` | `python scripts/rol07_verificacion.py` |
| 8 | ROL 8 · Benchmark y pruebas | Fredy Eduardo Villegas Pérez | 2 min | `ruta_optima/benchmark.py` y `tests/test_casos_borde.py` | `python scripts/rol08_benchmark.py` y `python -m pytest tests/test_casos_borde.py -v` |
| 9 | ROL 9 · Página web (demo) | Christian Raphael Valer Cusipaucar | 3 min | `web/app.js` y `app.py` | `python app.py` |
| 10 | ROL 10 · Conclusiones | Mario Jesús Ramírez Barriga | 1.5 min | `ruta_optima/config.py` | `python main.py --n 100 --vehiculos 12` |

**Total: unos 20 minutos** (el mínimo pedido es 10).

---

## 4. Guion de cada rol

Cada guion tiene tres partes: **A. Explicar el código**, **B. Ejecutarlo** y **C. Pasar la palabra**. Lo que está entre *(paréntesis)* es lo que haces en pantalla; lo que está entre comillas es lo que dices.

### ROL 1 – Luis Angel López Siccha · Problema y cómo está armado el proyecto (2.5 min)

**Abrir antes:** `README.md` en GitHub, `ruta_optima/solver.py` y `ruta_optima/evaluador.py`.

**Presentación (cámara, sin compartir):**
> «Hola, somos el equipo del curso Análisis de Algoritmos y Estrategias de Programación de la UPN. Nuestro proyecto es **Ruta Óptima de Última Milla en Lima**. Una empresa reparte paquetes con varios vehículos: cada uno carga hasta **100 paquetes**, cada cliente debe recibir su pedido dentro de una **ventana de 2 horas** y la ruta no puede durar más de **8 horas**. El costo es **S/ 1.20 por kilómetro más S/ 12.50 por hora**. Este problema se llama **VRPTW** y es **NP-difícil**: con solo 20 clientes ya hay más de 10¹⁸ órdenes posibles, así que no se pueden probar todos. Por eso comparamos **dos estrategias**: una **voraz** y otra que combina **divide y vencerás con programación dinámica**.»

**A. Explicar el código** *(compartir pantalla)*
- *(Mostrar el diagrama del README en GitHub.)* «El proyecto está dividido en módulos, y cada integrante se encargó de uno. Este diagrama muestra cómo se conectan.»
- *(Abrir `solver.py`, líneas 40–80, `resolver_estrategia_2`.)* «Aquí se juntan las piezas de la estrategia 2. En la línea 51 se divide la ciudad en **zonas**, en la 52 se **reparten las zonas entre los vehículos** y en la 63 se busca el **orden óptimo dentro de cada zona** con Held-Karp.»
- *(Bajar a las líneas 83–96, `comparar`.)* «Esta función corre **las dos estrategias sobre el mismo problema** y las evalúa.»
- *(Abrir `evaluador.py`, líneas 27–53, `evaluar_orden`.)* «Este es el **evaluador común**. Recorre la ruta y calcula la hora de llegada a cada cliente. En la línea 46, si el vehículo llega antes de la ventana, espera. En la línea 47, si llega tarde, la ruta no es válida. En la línea 51 comprueba que el vehículo vuelva al almacén dentro de la jornada. Como las dos estrategias pasan por el mismo evaluador, **la comparación es justa**.»

**B. Ejecutar**
```bash
python main.py --n 60
```
> «Primero el programa muestra el estado de cada módulo: todos están **LISTO**. Abajo compara las dos estrategias con **60 clientes y 9 vehículos**. Las dos son válidas. El voraz cuesta **S/ 1289.75** y atiende al **96.7 %**; divide y vencerás + PD cuesta **S/ 1323.05**, pero atiende al **100 %** de los clientes y usa un vehículo menos.»

```bash
python -m pytest
```
> «Y estas son nuestras pruebas automáticas: **71 pruebas, todas pasan**. También corren solas en GitHub cada vez que alguien sube cambios.»

**C. Pasar la palabra:** «Todo empieza por crear los problemas de prueba. Edgar, adelante.»

---

### ROL 2 – Edgar Ismael Victorio Capa · Instancias (1.5 min)

**Abrir antes:** `ruta_optima/generador.py`, `ruta_optima/instancias.py` y `resultados/instancias/pequena.json`.

**A. Explicar el código**
- *(`generador.py`, líneas 22–58, `generar_instancia`.)* «Una **instancia** es un problema concreto: el almacén y los clientes. Aquí se crean al azar: en la línea 38 el almacén va al centro de la ciudad, y en el bucle de la línea 41 cada cliente recibe su ubicación, su demanda de 1 a 6 paquetes, su ventana de 2 horas y su tiempo de atención.»
- *(Señalar la línea 36, `random.Random(semilla)`.)* «Lo más importante es la **semilla**: la misma semilla da siempre **exactamente el mismo problema**. Así cualquiera puede repetir nuestros experimentos.»
- *(`instancias.py`, líneas 18–30.)* «`guardar_instancia` convierte el problema a **JSON** y `cargar_instancia` lo vuelve a leer.»
- *(Líneas 33–57, `generar_instancia_distritos`.)* «Esta es una variante en la que los clientes se agrupan en **distritos**. En las líneas 49 y 50 se usa `random.gauss` para ubicarlos cerca del centro de cada distrito, como en una ciudad real.»

**B. Ejecutar**
```bash
python scripts/rol02_instancias.py
```
> «Se crean las tres instancias oficiales: **pequeña con 8 clientes, mediana con 40 y grande con 200**. Cada una se guarda en JSON y, al volver a cargarla, sale **"recarga idéntica: True"**, o sea que se guardó sin perder nada.»

*(Abrir `resultados/instancias/pequena.json`.)* «Aquí se ve el archivo: el almacén y cada cliente con sus datos.»

**C. Pasar la palabra:** «Ya tenemos los clientes. Ahora, ¿cuántos kilómetros hay entre ellos? Luis Fernando.»

---

### ROL 3 – Luis Fernando Reyes Casiano · Distancias con Dijkstra (2 min)

**Abrir antes:** `ruta_optima/distancias.py`.

**A. Explicar el código**
- *(Líneas 36–66, `construir_grafo_calles`.)* «Los camiones no van en línea recta, van por calles. Modelamos la ciudad como una **cuadrícula de calles de 1 km**: en las líneas 48 a 54 cada esquina se une con la de al lado. En las líneas 58 a 65 cada cliente se conecta a su esquina más cercana.»
- *(Líneas 19–33, `dijkstra`.)* «Para el camino más corto usamos **Dijkstra**. En la línea 23 creamos una **cola de prioridad** con `heapq`. En la línea 25 siempre sacamos el punto con **menor distancia conocida**. En la línea 26 ignoramos las entradas viejas. En las líneas 30 a 32 está la **relajación**: si encontramos un camino más corto a un vecino, lo actualizamos. La complejidad es **O((V + E) log V)**.»
- *(Líneas 69–78, `matriz_distancias`.)* «En la línea 75 ejecutamos Dijkstra **una vez por el almacén y una por cada cliente**, es decir n + 1 veces. Así llenamos la **matriz de distancias** que usan las dos estrategias.»

**B. Ejecutar**
```bash
python scripts/rol03_distancias.py
```
> «La primera línea es una prueba con un grafo pequeño: el resultado de Dijkstra es **igual al esperado**. Después calculamos la matriz para 20, 50, 100 y 200 clientes: incluso con **200 clientes tarda menos de 0.1 segundos**. La última columna compara con la línea recta: **la distancia por calles es un poco mayor**, como pasa en la realidad.»

**C. Pasar la palabra:** «Con las distancias listas, Cristofher explica cómo dividimos la ciudad.»

---

### ROL 4 – Cristofher Maguiña Peche · Zonas con divide y vencerás (2 min)

**Abrir antes:** `ruta_optima/zonas.py`, `resultados/zonas_k12.png` y `resultados/zonas_k6.png`.

**A. Explicar el código**
- *(Líneas 32–59, `dividir_en_zonas`.)* «La programación dinámica es exacta, pero muy lenta con muchos clientes. Por eso primero **dividimos**: es **divide y vencerás**. En la línea 42 está el **caso base**: si hay k clientes o menos, ya es una zona. Si no, en la línea 47 elegimos el eje donde los clientes están más dispersos, en la línea 51 calculamos la **mediana**, y en la línea 59 la función **se llama a sí misma** con cada mitad.»
- *(Líneas 10–29, `quickselect`.)* «La mediana la encontramos con **Quickselect**: elegimos un pivote, separamos en menores, iguales y mayores, y seguimos **solo por el lado** donde está la mediana. No hace falta ordenar todo, así que cuesta **O(n) en promedio**.»
- «La recurrencia es **T(n) = 2T(n/2) + O(n)**, que por el Teorema Maestro da **O(n log n)**.»

**B. Ejecutar**
```bash
python scripts/rol04_zonas.py
```
> «Con 60 clientes y **k = 12** salen **8 zonas** de 7 u 8 clientes. Con **k = 6** salen **16 zonas** de 3 o 4. Ninguna pasa de k y todas quedan equilibradas gracias a la mediana.»

*(Abrir `resultados/zonas_k12.png`.)* «Aquí se ve: cada color es una zona y el cuadrado negro es el almacén.»

**C. Pasar la palabra:** «Antes de ordenar cada zona, Carlo presenta la primera estrategia, la voraz.»

---

### ROL 5 – Carlo Stefano Soel Olivo · Estrategia voraz (2 min)

**Abrir antes:** `ruta_optima/voraz.py` y `resultados/atendidos_vs_vehiculos.png`.

**A. Explicar el código**
- *(Líneas 63–96, `ruta_voraz`.)* «Esta es la **estrategia 1**. En la línea 75 sale un vehículo a la vez. En las líneas 81 a 84 ordenamos a los clientes pendientes **del más cercano al más lejano**. En la línea 86 tomamos **el primero que sea factible** según el evaluador: que quepa en la carga, que llegue en su ventana y que pueda volver a tiempo. Si ninguno es factible, en la línea 92 el vehículo vuelve y sale el siguiente. Es **O(n²)**, muy rápida, pero **miope**: solo mira el paso inmediato.»
- *(Líneas 9–60, `asignar_zonas`.)* «También programamos el **reparto de zonas a vehículos** de la estrategia 2, que también es voraz. En la línea 36 ordenamos las zonas de la más trabajosa a la menos trabajosa, y en la línea 41 cada zona va al **vehículo con menos trabajo acumulado**. No llenamos un vehículo hasta 100 paquetes porque el **límite real es el tiempo** de la jornada.»

**B. Ejecutar**
```bash
python scripts/rol05_voraz.py
```
> «Probamos con 2, 4, 6 y hasta 15 vehículos. Con **2 vehículos** el voraz atiende al **14 %** y divide y vencerás al **25 %**. Con **12 vehículos**, **87.7 % contra 95 %**. Más vehículos, más clientes atendidos.»

*(Abrir `resultados/atendidos_vs_vehiculos.png`.)* «En el gráfico se ve que la línea de divide y vencerás va casi siempre por encima.»

**C. Pasar la palabra:** «Ahora Aldrin explica cómo encontramos el orden óptimo dentro de cada zona.»

---

### ROL 6 – Aldrin Juaquin Meliton Espinoza · Programación dinámica Held-Karp (2 min)

**Abrir antes:** `ruta_optima/held_karp.py` y `resultados/held_karp_tiempo.png`.

**A. Explicar el código**
- *(Líneas 17–21, comentario.)* «Dentro de cada zona usamos **programación dinámica** con el algoritmo de **Held-Karp**. La idea es una tabla **dp[máscara][j]**: la máscara es un número cuyos bits dicen qué clientes ya visitamos, y j es el último. En cada casilla guardamos la **hora más temprana** a la que podemos terminar en j.»
- *(Líneas 33–35.)* «Aquí creamos la tabla: hay **2^k** máscaras.»
- *(Líneas 38–41, caso base.)* «Caso base: ir directo a cada cliente. En la línea 39, con `max(…, ventana_ini)`, si el vehículo llega antes de que abra la ventana, **espera**.»
- *(Líneas 44–59, transición.)* «Transición: desde cada estado agregamos un cliente que falte. En la línea 54, si llegaría tarde, ese camino se descarta. Cada combinación se calcula **una sola vez** y se reutiliza: esa es la clave de la programación dinámica.»
- *(Líneas 73–80.)* «Al final reconstruimos el orden hacia atrás con la tabla `padre`. La complejidad es **O(k²·2^k)**.»

**B. Ejecutar**
```bash
python scripts/rol06_held_karp.py
```
> «Medimos el tiempo para zonas de 4 a 14 clientes. Con **12 clientes tarda unas pocas centésimas de segundo** y con **14, unos 0.2 segundos** *(lee los números que te salgan)*: cada cliente extra casi duplica el tiempo. Por eso lo usamos **solo dentro de zonas pequeñas**; con 200 clientes juntos sería imposible.»

*(Abrir `resultados/held_karp_tiempo.png`.)* «El gráfico muestra ese crecimiento exponencial.»

**C. Pasar la palabra:** «¿Y cómo sabemos que el orden es realmente el óptimo? Fredy lo comprueba.»

---

### ROL 7 – Fredy Abraham Núñez Cerdán · Verificación con fuerza bruta (1.5 min)

**Abrir antes:** `ruta_optima/fuerza_bruta.py` y `resultados/fuerza_bruta_vs_held_karp.png`.

**A. Explicar el código**
- *(Líneas 11–28, `mejor_orden_fuerza_bruta`.)* «La fuerza bruta resuelve **el mismo problema** que Held-Karp, pero de la forma más simple. En la línea 23, `itertools.permutations` genera **todos los órdenes posibles**. En la línea 25 cada orden se evalúa con el mismo evaluador, y en la línea 26 nos quedamos con el que termina más temprano. Es tan simple que no se puede equivocar, por eso sirve de **referencia**. Su complejidad es **O(k!)**.»

**B. Ejecutar**
```bash
python scripts/rol07_verificacion.py
```
> «La primera línea es la importante: **Held-Karp y fuerza bruta coinciden en 200 de 200 zonas al azar**. Eso demuestra que Held-Karp encuentra el óptimo. Abajo están los tiempos: con **9 clientes** la fuerza bruta tarda **medio segundo** y Held-Karp **unos milisegundos**. El factorial crece mucho más rápido que el exponencial.»

*(Abrir `resultados/fuerza_bruta_vs_held_karp.png`.)*

**C. Pasar la palabra:** «Ya sabemos que todo funciona bien. Fredy Villegas muestra los resultados completos.»

---

### ROL 8 – Fredy Eduardo Villegas Pérez · Benchmark y casos extremos (2 min)

**Abrir antes:** `ruta_optima/benchmark.py`, `tests/test_casos_borde.py` y `resultados/costo_vs_n.png`.

**A. Explicar el código**
- *(`benchmark.py`, líneas 24–50, `ejecutar_benchmark`.)* «Para comparar en serio corremos muchos casos. En las líneas 33 y 34 recorremos los **tamaños** (20, 50, 100, 150 y 200 clientes) y **5 semillas** por tamaño. En la línea 36 comparamos las dos estrategias y en la línea 37 guardamos el costo, los km, el % atendidos y el tiempo. Al final, en la línea 48, se guarda el CSV y se hacen los gráficos. Usamos 5 semillas porque **un solo caso puede salir con suerte**.»
- *(`tests/test_casos_borde.py`, las dos últimas pruebas.)* «También probamos **casos extremos**. En `test_capacidad_insuficiente` los vehículos no alcanzan para toda la demanda, y comprobamos que el programa no falla y reporta clientes no atendidos. En `test_ventanas_imposibles` todos los clientes cierran a las 00:01, y comprobamos que no se atiende a nadie y que la solución sigue siendo válida.»

**B. Ejecutar**
```bash
python scripts/rol08_benchmark.py
```
> «Tarda unos segundos. *(esperar)* La tabla muestra el promedio. Con **50 clientes**, divide y vencerás + PD cuesta **S/ 993.90 contra S/ 1117.95** del voraz y atiende más: **92.4 % contra 87.2 %**. Con **150 clientes** el voraz sale más barato, pero porque atiende a menos: **77.3 % contra 90.9 %**. Abajo está el efecto de k: con **k = 14** el costo baja a **S/ 1495.57**, pero el tiempo sube. Por eso usamos k = 12.»

```bash
python -m pytest tests/test_casos_borde.py -v
```
> «Las **5 pruebas de casos extremos pasan**.»

*(Abrir `resultados/costo_vs_n.png`.)*

**C. Pasar la palabra:** «Ahora Christian lo muestra todo funcionando en la página web.»

---

### ROL 9 – Christian Raphael Valer Cusipaucar · Página web en vivo (3 min)

**Abrir antes:** `web/app.js`, `app.py` y una terminal.

**A. Explicar el código**
- *(`web/app.js`, líneas 31–45, `calcular`.)* «La página está hecha con HTML, CSS y JavaScript. Al presionar **Calcular rutas**, en la línea 35 se hace un `fetch` a `/api/resolver` y se envían los parámetros: clientes, vehículos, k y semilla.»
- *(`app.py`, líneas 146–155, `do_POST`.)* «Python recibe ese pedido en un pequeño servidor web, lee los datos y llama a `resolver`.»
- *(Líneas 45–60, `resolver`.)* «`resolver` crea el problema en la línea 53, calcula las distancias en la 54 y corre **las dos estrategias** en las líneas 56 a 58. Después devuelve todo en **JSON** para que la página lo dibuje.»

**B. Ejecutar**
```bash
python app.py
```
*(Se abre el navegador en http://localhost:8000. Si no se abre solo, escribir esa dirección.)*

1. *(Dejar 40 clientes, 6 vehículos, k = 12 y semilla 42, y presionar **Calcular rutas**.)*
   > «Con **40 clientes y 6 vehículos**, divide y vencerás + PD cuesta **S/ 660.88 contra S/ 822.58** del voraz, usa **4 vehículos en vez de 6** y atiende al **77.5 % contra 72.5 %**. En verde está la mejor en cada fila.»
2. *(Marcar **Mostrar las zonas**.)*
   > «En los mapas, cada color es la ruta de un vehículo, el cuadrado negro es el almacén y **los puntos rojos son clientes que no se pudieron atender**. Con esta casilla se ven de fondo las **zonas** de divide y vencerás.»
3. *(Abrir la pestaña **Detalle de rutas**.)*
   > «Aquí está cada vehículo con la **hora de llegada**, cuánto **espera** y la **ventana** de cada cliente.»
4. *(Abrir la pestaña **Experimentos**.)*
   > «Y aquí están los gráficos del benchmark que mostró Fredy.»
5. *(Volver a **Comparación**, marcar **Clientes agrupados por distritos**, poner **80 clientes** y calcular. Para llegar justo a 80, haz clic en la barra y usa las flechas del teclado; los vehículos cambian solos a 12.)*
   > «Con clientes agrupados por distritos, como en una ciudad real, las dos estrategias atienden al 100 % y divide y vencerás sale más barata.»
6. *(Para cerrar la página: `Ctrl + C` en la terminal.)*

**C. Pasar la palabra:** «Para terminar, Mario presenta las conclusiones.»

---

### ROL 10 – Mario Jesús Ramírez Barriga · Conclusiones (1.5 min)

**Abrir antes:** `ruta_optima/config.py` y `docs/RESULTADOS.md`.

**A. Explicar el código**
- *(`config.py`.)* «Todos los parámetros del problema están en un solo archivo, `config.py`: **capacidad de 100**, **jornada de 8 horas**, **15 vehículos como máximo**, ventanas de **2 horas**, velocidad de **25 km/h**, costos de **S/ 1.20 por km y S/ 12.50 por hora**, y **k = 12**. Son los mismos valores de la Tabla 1 de nuestro informe.»

**B. Ejecutar**
```bash
python main.py --n 100 --vehiculos 12
```
> «Una última prueba con **100 clientes y 12 vehículos**. El voraz cuesta **S/ 1713.75** pero solo atiende al **70 %**. Divide y vencerás + PD cuesta **S/ 1914.24** y atiende al **96 %**. Si dividimos el costo entre los clientes atendidos, la segunda estrategia sale **más barata por cliente**: unos S/ 20 contra S/ 24.»

**Conclusiones** *(puede ser con la cámara, sin compartir)*
> «En conclusión, **ninguna estrategia gana en todo**. El **voraz** es más simple y rapidísimo, pero miope. **Divide y vencerás + programación dinámica** atiende a más clientes y casi siempre cuesta menos por cliente, y tarda alrededor de un décimo de segundo como máximo. Para una empresa de reparto conviene la segunda.
>
> Además vimos en la práctica la teoría del curso: Dijkstra en O((V + E) log V), divide y vencerás en O(n log n), programación dinámica en O(k²·2^k) y fuerza bruta en O(k!).
>
> Nuestras **limitaciones**: las calles son simuladas, la velocidad es constante y no hay tráfico, hay un solo almacén, y las zonas no tienen en cuenta los horarios. Como **trabajo futuro** proponemos agrupar también por horario, usar mapas reales de Lima y mejorar las rutas con búsqueda local.
>
> Todo el código está en nuestro repositorio de GitHub. **Muchas gracias.**»

*(Luis Angel detiene la grabación.)*

---

## 5. Lista final antes de grabar

- [ ] Todos hicieron `git pull origin main` y `python -m pip install -r requirements.txt`.
- [ ] Cada uno ejecutó **su comando** una vez y le salió lo mismo que en esta guía.
- [ ] Christian comprobó que `python app.py` abre la página.
- [ ] Cada uno tiene su archivo abierto en VS Code y su imagen de `resultados/` a mano.
- [ ] Luis Angel tiene la grabación de Meet lista.
