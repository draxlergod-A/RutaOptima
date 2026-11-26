# Guía de la exposición final (≈ 15 minutos)

Cada integrante expone **su parte** en 1 a 2 minutos. La demo en vivo (ROL 9) dura un poco más.
No hace falta memorizar: **lee el guion una o dos veces y dilo con tus palabras**. Las cifras salen de nuestro benchmark (`docs/RESULTADOS.md`) y de los scripts de cada rol.

## Orden de exposición y tiempos

| # | Rol | Tema | Quién | Tiempo | Qué se muestra en pantalla |
|---|---|---|---|---|---|
| 1 | ROL 1 | Problema, objetivo y cómo está armado el proyecto | Luis Angel López Siccha | 2 min | README del repositorio en GitHub (diagrama y tablero) |
| 2 | ROL 2 | Instancias de prueba | Edgar Ismael Victorio Capa | 1 min | `resultados/instancias/mediana.json` |
| 3 | ROL 3 | Distancias por calles (Dijkstra) | Luis Fernando Reyes Casiano | 1.5 min | `ruta_optima/distancias.py` y `resultados/rol03_distancias.csv` |
| 4 | ROL 4 | Zonas con divide y vencerás | Cristofher Maguiña Peche | 1.5 min | `resultados/zonas_k12.png` y `zonas_k6.png` |
| 5 | ROL 5 | Estrategia voraz | Carlo Stefano Soel Olivo | 1.5 min | `resultados/atendidos_vs_vehiculos.png` |
| 6 | ROL 6 | Programación dinámica (Held-Karp) | Aldrin Juaquin Meliton Espinoza | 1.5 min | `resultados/held_karp_tiempo.png` |
| 7 | ROL 7 | Verificación con fuerza bruta | Fredy Abraham Núñez Cerdán | 1 min | `resultados/fuerza_bruta_vs_held_karp.png` |
| 8 | ROL 8 | Resultados del benchmark | Fredy Eduardo Villegas Pérez | 1.5 min | `docs/RESULTADOS.md` y `resultados/costo_vs_n.png` |
| 9 | ROL 9 | **Demo en vivo de la página web** | Christian Raphael Valer Cusipaucar | 2.5 min | La página (`python app.py`) |
| 10 | ROL 10 | Conclusiones y limitaciones | Mario Jesús Ramírez Barriga | 1.5 min | Tabla de `docs/RESULTADOS.md` |
| | | Preguntas del docente | Todos | 2–5 min | |

**Total: unos 15 minutos** con preguntas (mínimo pedido: 10).

## Antes de empezar (5 minutos antes)

1. **Luis Angel comparte pantalla** durante toda la exposición y abre lo que dice la columna «Qué se muestra». Así nadie pierde tiempo buscando archivos.
2. Tener abiertas, cada una en su pestaña: el repositorio en GitHub, la carpeta `resultados/` y la página web (`python app.py` → http://localhost:8000).
3. **Christian** comprueba antes que `python app.py` abre la página en su PC. Si falla, Luis Angel hace la demo desde la suya.
4. Cámara encendida y micrófono en silencio cuando no te toca hablar.
5. Cada uno termina con la **frase para pasar la palabra** (está en su guion), así no hay silencios.

---

## Guiones

### ROL 1 – Luis Angel López Siccha · Problema y proyecto (2 min)
**Mostrar:** el README en GitHub (el diagrama de flujo y el tablero de roles).

> «Buenas tardes. Nuestro proyecto es **Ruta Óptima de Última Milla en Lima**. El problema es el de una empresa que reparte paquetes en la ciudad. Tiene varios vehículos y cada uno carga hasta **100 paquetes**. Cada cliente debe recibir su pedido dentro de una **ventana de 2 horas**, y cada ruta no puede durar más de **8 horas**. El costo es **S/ 1.20 por kilómetro más S/ 12.50 por hora**.
>
> Este problema se llama VRPTW y es **NP-difícil**: las rutas posibles crecen de forma factorial, así que no se pueden probar todas. Por eso comparamos **dos estrategias** sobre los mismos problemas. La primera es **voraz**: siempre va al cliente más cercano. La segunda combina **divide y vencerás con programación dinámica**: primero parte la ciudad en zonas pequeñas y luego encuentra el orden óptimo dentro de cada zona.
>
> Para que la comparación sea justa, las dos estrategias usan el **mismo evaluador**, que revisa capacidad, ventanas y jornada, y calcula el costo. El código está en GitHub, dividido en módulos, y cada integrante se encargó de uno, que es lo que van a explicar ahora. Además tiene **71 pruebas automáticas** que pasan todas.
>
> Empezamos por cómo se crean los problemas de prueba. Te paso la palabra, Edgar.»

**Si te preguntan «¿por qué NP-difícil?»:** porque contiene al problema del viajante. Con 20 clientes ya hay más de 10¹⁸ órdenes posibles.

---

### ROL 2 – Edgar Ismael Victorio Capa · Instancias (1 min)
**Mostrar:** `resultados/instancias/mediana.json` abierto (se ven el almacén y los clientes con sus datos).

> «Una **instancia** es un problema concreto: dónde está el almacén y, por cada cliente, su ubicación, cuántos paquetes pide, su ventana de horario y su tiempo de atención.
>
> Las generamos al azar pero con una **semilla**: la misma semilla siempre da exactamente el mismo problema, gracias a `random.Random(semilla)`. Esto es importante porque así cualquiera puede repetir nuestros experimentos y obtener los mismos números.
>
> Además las **guardamos en archivos JSON**. Tenemos tres oficiales: pequeña con **8 clientes**, mediana con **40** y grande con **200**. También hay una versión con los clientes **agrupados por distritos**, que se parece más a una ciudad real.
>
> Ahora, para saber cuánto hay de un cliente a otro, Luis Fernando explica las distancias.»

**Si te preguntan «¿para qué el JSON?»:** para guardar el problema y volver a usarlo sin generarlo otra vez, y para comparar las dos estrategias sobre exactamente el mismo caso.

---

### ROL 3 – Luis Fernando Reyes Casiano · Distancias con Dijkstra (1.5 min)
**Mostrar:** la función `dijkstra` en `ruta_optima/distancias.py` y luego `resultados/rol03_distancias.csv`.

> «Los camiones no viajan en línea recta, sino por calles. Por eso modelamos la ciudad como una **cuadrícula de calles de 1 km** y conectamos a cada cliente con su esquina más cercana.
>
> Para encontrar el camino más corto usamos el **algoritmo de Dijkstra**. Tiene una **cola de prioridad** (`heapq`) que siempre saca el punto con la menor distancia conocida, así que cuando un punto sale de la cola su distancia ya es la mínima. Su complejidad es **O((V + E) log V)**.
>
> Lo ejecutamos **n + 1 veces**, una desde el almacén y una desde cada cliente, y así armamos la **matriz de distancias** que usan las dos estrategias. Con 200 clientes tarda **menos de 0.1 segundos**. Como se ve en el CSV, la distancia por calles es un poco mayor que la línea recta, como pasa en la realidad.
>
> Con las distancias listas, Cristofher explica cómo dividimos la ciudad en zonas.»

**Si te preguntan «¿por qué la distancia por calles es mayor?»:** porque solo se avanza por calles de este a oeste o de norte a sur; para ir en diagonal hay que hacer «escalones».

---

### ROL 4 – Cristofher Maguiña Peche · Zonas con divide y vencerás (1.5 min)
**Mostrar:** `resultados/zonas_k12.png` y luego `resultados/zonas_k6.png`.

> «La programación dinámica que usamos es exacta, pero se vuelve muy lenta con muchos clientes. Por eso primero **dividimos el problema**: esa es la técnica **divide y vencerás**.
>
> Miramos si los clientes están más dispersos de izquierda a derecha o de arriba a abajo, y **cortamos por la mediana** en esa dirección, quedando dos mitades iguales. La mediana la calculamos con **Quickselect**, que la encuentra sin ordenar todo, en **O(n) promedio**. Repetimos el corte en cada mitad hasta que cada zona tenga **12 clientes o menos**.
>
> En la imagen, con 60 clientes y k = 12 salen **8 zonas** de 7 u 8 clientes, cada color es una zona. Con k = 6 salen 16 zonas más pequeñas.
>
> La recurrencia es **T(n) = 2T(n/2) + O(n)** y, por el Teorema Maestro, da **O(n log n)**.
>
> Antes de ver qué pasa dentro de cada zona, Carlo explica la estrategia voraz.»

**Si te preguntan «¿por qué la mediana?»:** porque parte en dos mitades iguales; así las zonas quedan equilibradas y ninguna pasa de k clientes.

---

### ROL 5 – Carlo Stefano Soel Olivo · Estrategia voraz (1.5 min)
**Mostrar:** `resultados/atendidos_vs_vehiculos.png`.

> «La primera estrategia es **voraz**: en cada paso el vehículo va al **cliente más cercano que sea factible**, es decir, que quepa en la carga, al que llegue dentro de su ventana y desde el que pueda volver al almacén antes de que termine la jornada. Cuando ya no puede atender a nadie más, vuelve y sale el siguiente vehículo. Es muy rápida, **O(n²)**, y resuelve en milisegundos.
>
> Su problema es que es **miope**: solo mira el paso inmediato. Por eso suele dejar a los clientes lejanos para el final y termina cruzando la ciudad.
>
> También programamos el **reparto de zonas a vehículos** de la segunda estrategia. Descubrimos que llenar cada vehículo hasta 100 paquetes no sirve, porque el **límite real es el tiempo** de la jornada, no la capacidad. Por eso el trabajo se reparte de forma equilibrada. En el gráfico se ve que con más vehículos se atiende a más clientes.
>
> Ahora Aldrin explica cómo encontramos el orden óptimo dentro de cada zona.»

**Si te preguntan «¿por qué el voraz no da siempre la mejor ruta?»:** porque elige lo mejor del momento sin mirar el futuro; ir al más cercano ahora puede obligar a un viaje muy largo después.

---

### ROL 6 – Aldrin Juaquin Meliton Espinoza · Programación dinámica Held-Karp (1.5 min)
**Mostrar:** `resultados/held_karp_tiempo.png`.

> «Dentro de cada zona usamos **programación dinámica** con el algoritmo de **Held-Karp**, que encuentra el **orden óptimo** de visita.
>
> La idea es una tabla **dp[máscara][j]**. La máscara indica qué clientes ya visitamos y j es el último. En cada casilla se guarda la **hora más temprana** a la que podemos terminar de atender a j. Cada combinación se calcula **una sola vez** y se reutiliza: esa es la clave de la programación dinámica. Si el vehículo llega antes de que abra la ventana del cliente, **espera**; si llega tarde, ese orden se descarta.
>
> Su complejidad es **O(k²·2^k)**. En el gráfico se ve que cada cliente más casi duplica el tiempo: con 12 clientes tarda unos **0.03 segundos** y con 14 unos **0.24 segundos**. Con 200 clientes juntos sería imposible, por eso solo lo usamos dentro de zonas de 12 o menos.
>
> ¿Y cómo sabemos que de verdad es óptimo? Eso lo explica Fredy.»

**Si te preguntan «¿qué es la máscara?»:** un número cuyos bits encendidos dicen qué clientes ya se visitaron; por ejemplo 0101 significa que se visitaron el cliente 0 y el 2.

---

### ROL 7 – Fredy Abraham Núñez Cerdán · Verificación con fuerza bruta (1 min)
**Mostrar:** `resultados/fuerza_bruta_vs_held_karp.png`.

> «Para confiar en Held-Karp lo comparamos con **fuerza bruta**, que prueba **todos los órdenes posibles**. Es lento pero tan simple que no se puede equivocar, así que sirve de referencia.
>
> Probamos **200 zonas al azar** y los dos dieron **exactamente el mismo resultado en las 200**. Eso nos da confianza en que Held-Karp encuentra el óptimo.
>
> El gráfico muestra la diferencia de velocidad: con 9 clientes la fuerza bruta tarda cerca de **medio segundo** y Held-Karp unos **2 milésimos**. La fuerza bruta es **O(k!)**, factorial, y Held-Karp es **O(k²·2^k)**: el factorial crece mucho más rápido.
>
> Ahora que sabemos que todo funciona, Fredy Villegas muestra los resultados.»

---

### ROL 8 – Fredy Eduardo Villegas Pérez · Resultados del benchmark (1.5 min)
**Mostrar:** la tabla de `docs/RESULTADOS.md` y luego `resultados/costo_vs_n.png`.

> «Corrimos las dos estrategias con **20, 50, 100, 150 y 200 clientes**, cada una con **5 semillas distintas**, y promediamos. Usamos 5 semillas porque un solo caso puede salir con suerte.
>
> **Divide y vencerás + PD** fue más barato con 20, 50 y 100 clientes. Por ejemplo, con 50 clientes costó **S/ 994 contra S/ 1118** del voraz. También atendió a más clientes en casi todos los tamaños: con 150 clientes, **91 % contra 77 %**. Con 100 clientes el voraz atendió un poco más.
>
> Con 150 y 200 clientes el voraz sale más barato, pero **porque atiende a menos clientes**. El voraz siempre es el más rápido, en milisegundos, aunque la otra estrategia tampoco tarda mucho: **alrededor de 0.1 segundos** como máximo.
>
> Probamos además el tamaño de zona k: con k = 14 el costo baja a **S/ 1496**, pero el tiempo sube. Por eso usamos k = 12. Y agregamos pruebas de casos extremos, como poca capacidad y horarios imposibles, que el sistema maneja sin errores.
>
> Ahora Christian lo muestra en vivo.»

**Si te preguntan «¿por qué con 200 clientes ninguna atiende a todos?»:** porque 15 vehículos de 8 horas no alcanzan; el límite es la flota, no el algoritmo.

---

### ROL 9 – Christian Raphael Valer Cusipaucar · Demo en vivo (2.5 min)
**Mostrar:** la página web (`python app.py`). **Plan B:** si la página no abre, mostrar las capturas de `docs/capturas/`.

> «Esta es nuestra página. Con `python app.py` se abre en el navegador. A la izquierda elegimos los parámetros: dejo **40 clientes y 6 vehículos** y presiono **Calcular rutas**.» *(presionar)*
>
> «Arriba sale el resumen y la tabla comparativa, y **en verde está la mejor** en cada fila. En este caso divide y vencerás + PD cuesta **S/ 660.88 contra S/ 822.58** del voraz, usa **4 vehículos en vez de 6** y atiende al **77.5 % contra 72.5 %**.» *(señalar la tabla)*
>
> «Abajo están los dos mapas: cada color es la ruta de un vehículo, el cuadrado negro es el almacén y **los puntos rojos son clientes que no se pudieron atender**. Si marco **Mostrar las zonas**, se ven en colores de fondo las zonas de divide y vencerás.» *(marcar la casilla)*
>
> «En **Detalle de rutas** vemos, por cada vehículo, la hora de llegada, cuánto espera y la ventana de cada cliente.» *(abrir la pestaña)* «Y en **Experimentos** están los gráficos del benchmark.» *(abrir la pestaña)*
>
> «Por último, el botón **Otra instancia** genera un problema nuevo al azar.» *(presionarlo una vez)*
>
> «Para cerrar, Mario presenta las conclusiones.»

**Si te preguntan «¿cómo se comunica la página con Python?»:** la página hace un `fetch` a `/api/resolver`, Python ejecuta los algoritmos y responde en JSON.

---

### ROL 10 – Mario Jesús Ramírez Barriga · Conclusiones (1.5 min)
**Mostrar:** la tabla de `docs/RESULTADOS.md`.

> «Como conclusión, **ninguna estrategia gana en todo**. **Divide y vencerás + programación dinámica** da rutas más baratas en casos pequeños y medianos y atiende a más clientes. El **voraz** es más rápido y más simple, pero miope. Para una empresa conviene la segunda: tarda alrededor de un décimo de segundo y ahorra dinero.
>
> Además comprobamos la teoría del curso en la práctica: Dijkstra con O((V+E) log V), divide y vencerás con O(n log n), la programación dinámica con O(k²·2^k) y la fuerza bruta con O(k!).
>
> Las **limitaciones** del modelo: las calles son simuladas y no un mapa real, la velocidad es constante y sin tráfico, hay un solo almacén, y las zonas se forman solo por ubicación, sin mirar los horarios.
>
> Como **trabajo futuro**: agrupar también por horario, usar mapas reales de Lima y mejorar las rutas con búsqueda local.
>
> Muchas gracias. Quedamos atentos a sus preguntas.»

---

## Preguntas probables del docente (cualquiera puede responder)

1. **¿Por qué es NP-difícil?** Porque contiene al problema del viajante; las rutas posibles crecen factorialmente. → ROL 1
2. **¿Por qué Held-Karp solo dentro de zonas?** Su costo crece como 2^k; con 200 clientes juntos no alcanzan ni la memoria ni el tiempo. → ROL 6
3. **¿Cómo saben que Held-Karp es óptimo?** Se comparó contra fuerza bruta en 200 casos y coincidió en todos. → ROL 7
4. **¿Qué pasa con los clientes que no se pueden atender?** Quedan como «no atendidos» y se reportan (% atendidos); salen en rojo en el mapa. → ROL 9
5. **¿Qué pasaría con más vehículos?** Sube el % de atendidos (gráfico `atendidos_vs_vehiculos.png`). → ROL 5
6. **¿Cómo verificaron que las rutas cumplen las restricciones?** Un evaluador común revisa capacidad, ventanas y jornada de cada ruta, y hay 71 pruebas automáticas que corren en GitHub Actions. → ROL 1 / ROL 8
7. **¿Por qué k = 12?** Es el equilibrio entre costo y tiempo: con k = 14 el costo baja, pero el tiempo casi se triplica. → ROL 8
