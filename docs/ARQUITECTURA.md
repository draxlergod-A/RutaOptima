# Arquitectura y contratos

Todo el equipo programa contra los mismos contratos. **No cambies firmas ni unidades** sin avisar al ROL 1.

## Convenciones

| Tema | Convención |
|---|---|
| Almacén | `id = 0`. Los clientes son `1..n` (consecutivos). |
| Matrices | `(n+1) x (n+1)` indexadas por **id**: `dist[i][j]` km, `tiempos[i][j]` minutos. |
| Tiempo | minutos desde las 00:00 (09:00 = 540). `utilidades.hhmm(540)` → `"09:00"`. |
| Ruta | lista de ids de clientes **sin** el almacén: `[3, 7, 1]` significa 0→3→7→1→0. |
| Solución | `Solucion(nombre, rutas, no_atendidos, tiempo_ejecucion_s)` |
| Parámetros | todos en `ruta_optima/config.py`. Nunca escribas números mágicos en tu código. |

## Reglas del problema (las valida `evaluador.evaluar`)

1. Cada cliente se atiende **una sola vez** o queda en `no_atendidos`.
2. La suma de demandas de una ruta no supera la **capacidad** (100).
3. Se llega a cada cliente **antes** de que cierre su ventana; si se llega antes de que abra, se **espera**.
4. El vehículo sale a las 09:00 y **vuelve al almacén antes de** `hora_salida + jornada_max` (8 h).
5. Hay a lo sumo `num_vehiculos` rutas.
6. Costo = S/ 1.20 por km + S/ 12.50 por hora de operación.

## Quién llama a quién

```
solver.comparar(inst, k)
 ├─ distancias.matriz_distancias(inst)           ROL 3  -> dist ; utilidades.a_tiempos -> tiempos
 ├─ Estrategia 1: voraz.ruta_voraz(...)          ROL 5
 └─ Estrategia 2:
      zonas.dividir_en_zonas(clientes, k)        ROL 4  (usa quickselect)
      voraz.asignar_zonas(zonas, inst, tiempos)  ROL 5
      held_karp.ordenar_zona(zona, ...)          ROL 6  (por vehículo, encadenando origen y hora)
 └─ evaluador.evaluar(...)                       ROL 1  (juez común)
```

`evaluador.evaluar_orden(inst, orden, tiempos, origen, t_inicio)` es la **única** definición de «ruta factible y a qué hora termina». Held-Karp, fuerza bruta, voraz y las pruebas usan la misma, y por eso sus resultados se pueden comparar.

## Página web
`app.py` es un servidor pequeño (solo librería estándar de Python). La página `web/` envía los parámetros a `POST /api/resolver` y `app.py` llama a `solver` y `evaluador`; devuelve JSON con las rutas, horas de llegada y métricas, y `web/app.js` las dibuja en SVG.

## Pruebas
Cada módulo tiene su archivo en `tests/`. `python -m pytest` corre todo (69 pruebas pasan; 2 quedan marcadas `skip` hasta que el ROL 8 las complete).

## Decisiones de diseño (para el informe)

- **Reparto equilibrado de zonas (LPT)** en vez de llenar un vehículo hasta su capacidad: con capacidad 100 y demandas de 1 a 6, casi todos los clientes caben en uno o dos vehículos, pero el límite real es el **tiempo** (jornada de 8 h y ventanas de 2 h). Repartir el trabajo entre todos los vehículos disponibles atiende muchos más clientes. Con la versión «best-fit» de capacidad se atendía ~35 % en instancias de 100–200 clientes y con el reparto equilibrado sube bastante.
- **Zona infactible**: si Held-Karp devuelve `None`, el solver parte la zona en mitades y reintenta; un cliente solo imposible va a `no_atendidos`.
- **Held-Karp con k = 12** tarda milisegundos en estas instancias (las ventanas podan muchos estados); la memoria crece como 2^k.
