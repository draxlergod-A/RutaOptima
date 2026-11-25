# Guion de la presentación (≈ 10 minutos)

Cada integrante habla **1 minuto** sobre su parte (puede leer su guion, pero con sus palabras). Las cifras son de nuestro benchmark (`docs/RESULTADOS.md`); si vuelven a correrlo en su PC pueden variar un poco.

## Orden de exposición
| # | Rol | Tema | Quién |
|---|---|---|---|
| 1 | ROL 1 | Problema, objetivo y arquitectura del proyecto | Luis Angel López Siccha |
| 2 | ROL 2 | Instancias | _(nombre)_ |
| 3 | ROL 3 | Distancias y Dijkstra | _(nombre)_ |
| 4 | ROL 4 | Zonas (divide y vencerás) | _(nombre)_ |
| 5 | ROL 5 | Estrategia voraz | _(nombre)_ |
| 6 | ROL 6 | Programación dinámica | _(nombre)_ |
| 7 | ROL 7 | Verificación con fuerza bruta | _(nombre)_ |
| 8 | ROL 8 | Resultados del benchmark | _(nombre)_ |
| 9 | ROL 9 | **Demo en vivo de la página** | _(nombre)_ |
| 10 | ROL 10 | Conclusiones y limitaciones | _(nombre)_ |

## Guiones de 1 minuto

**ROL 1 – Problema.** Una empresa reparte paquetes en Lima. Cada vehículo carga hasta 100 unidades, cada cliente tiene una ventana de 2 horas, la jornada dura 8 horas y el costo es S/ 1.20 por km más S/ 12.50 por hora. Es un problema NP-difícil (VRPTW): no se puede probar todas las rutas. Comparamos dos estrategias sobre las mismas instancias: una voraz y otra que combina divide y vencerás con programación dinámica. Un evaluador común decide si una ruta es válida, así la comparación es justa.

**ROL 2 – Instancias.** Una instancia es un problema concreto: almacén, clientes con demanda, ventana y tiempo de servicio. Se generan con una semilla, por eso la misma semilla da exactamente el mismo problema. Podemos guardarlas en JSON y tenemos 3 oficiales: 8, 40 y 200 clientes. También hay una versión con clientes agrupados por distritos, más parecida a una ciudad real.

**ROL 3 – Distancias.** Los camiones no van en línea recta: modelamos la ciudad como una cuadrícula de calles de 1 km y calculamos el camino mínimo con Dijkstra usando una cola de prioridad, O((V+E) log V). Lo ejecutamos una vez por cliente y obtenemos una matriz de distancias; con 200 clientes tarda menos de 0.1 s. Las distancias por calles son un poco mayores que la línea recta, como en la realidad.

**ROL 4 – Zonas.** Held-Karp es exacto pero explota con muchos clientes, así que primero dividimos. Elegimos el eje con más dispersión, cortamos por la mediana (calculada con Quickselect, O(n) promedio) y repetimos hasta que cada zona tenga 12 clientes o menos. La recurrencia T(n)=2T(n/2)+O(n) da O(n log n).

**ROL 5 – Voraz.** La estrategia 1 va siempre al cliente más cercano que sea factible: que quepa en la carga, llegue en su ventana y pueda volver en la jornada. Es rápida (milisegundos) pero miope: deja clientes lejanos para el final. También reparte las zonas entre vehículos de forma equilibrada: descubrimos que llenar un vehículo por capacidad no sirve porque el límite real es el tiempo.

**ROL 6 – Programación dinámica.** Dentro de cada zona usamos Held-Karp: guardamos, para cada subconjunto de clientes y cada último cliente, el instante más temprano en que se puede terminar. Si el vehículo llega antes de abrir la ventana, espera. Complejidad O(k²·2^k): con k = 12 tarda unas 0.04 s y con k = 14 unas 0.2 s, por eso limitamos el tamaño de las zonas.

**ROL 7 – Verificación.** Para confiar en Held-Karp lo comparamos con fuerza bruta, que prueba todas las permutaciones, O(k!). Con 200 zonas al azar de 2 a 7 clientes dieron exactamente el mismo óptimo en las 200. Con k = 9 la fuerza bruta tarda cerca de 0.6 s y Held-Karp unos 0.003 s: se ve la diferencia entre factorial y exponencial.

**ROL 8 – Resultados.** Probamos de 20 a 200 clientes con 5 semillas. Divide y vencerás + PD tuvo menor costo en 20, 50 y 100 clientes (por ejemplo, S/ 994 vs S/ 1118 con 50) y atendió más clientes en 20, 50, 150 y 200; con 100 el voraz atendió un poco más (97.8 % vs 95 %). A cambio el voraz es mucho más rápido (milisegundos). Con 200 clientes y 15 vehículos ambas estrategias se quedan sin tiempo: la flota es el límite. Además, el tamaño de zona k influye: con k = 14 el costo baja pero el tiempo sube.

**ROL 9 – Demo.** Abrimos la página con `python app.py`. Elegimos 40 clientes y 6 vehículos y calculamos. Mostramos la tabla comparativa (en verde la mejor), los dos mapas con una ruta por color, los clientes en rojo que no se pudieron atender, y activamos «Mostrar zonas» para ver la división. En «Detalle de rutas» se ve la hora de llegada, la espera y la ventana de cada cliente.

**ROL 10 – Conclusiones.** Ninguna estrategia gana en todo: divide y vencerás + PD suele dar rutas más baratas y atiende a más clientes, y el voraz es más rápido y simple. Limitaciones: calles simuladas, velocidad constante, sin tráfico, un solo almacén y zonas que no miran las ventanas de tiempo. Trabajo futuro: agrupar por ventanas además de por ubicación, usar mapas reales y mejorar las rutas con búsqueda local.

## Preguntas probables
1. ¿Por qué es NP-difícil? Porque incluye el problema del viajante; las rutas posibles crecen factorialmente.
2. ¿Por qué Held-Karp solo dentro de zonas? Su costo crece como 2^k; con 200 clientes juntos no cabe en memoria ni tiempo.
3. ¿Cómo saben que Held-Karp es óptimo? Se verificó contra fuerza bruta en 200 casos.
4. ¿Qué pasa con los clientes que no se pueden atender? Quedan en «no atendidos» y se reportan (% atendidos).
5. ¿Qué pasaría con más vehículos? Sube el % atendidos (ver `resultados/atendidos_vs_vehiculos.png` del ROL 5).
