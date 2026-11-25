# ROL 3: Distancias por calles (Dijkstra)

El módulo que calcula los kilómetros reales por una red de calles con el algoritmo de Dijkstra.

> **El código ya está terminado y probado.** Tu tarea es corta: ejecutar, entender tu parte, guardar la evidencia y poder explicarla.

| | |
|---|---|
| **Tu rama** | `feature/rol03-distancias` |
| **Tu parte en el código** | `ruta_optima/distancias.py` |
| **Tiempo estimado** | 30–45 minutos |

## Paso 1. Preparar (una sola vez)
```bash
git clone <URL-DEL-REPOSITORIO>
cd ruta-optima-ultima-milla
git checkout feature/rol03-distancias
python -m pip install -r requirements.txt
```
Si Git dice que la rama no existe, créala: `git checkout -b feature/rol03-distancias`.

## Paso 2. Ejecutar
```bash
scripts/rol03_distancias.py
```
Debe terminar sin errores y mostrar resultados en la terminal. Si falla, mira `EJECUTAR.md` (sección «Si algo falla»).

## Paso 3. Qué debes guardar (entrega)
- `resultados/rol03_distancias.csv`

## Paso 4. Entiende tu parte (te la van a preguntar)
Abre el archivo indicado, lee los comentarios y responde estas preguntas **con tus palabras** en la sección «Mis respuestas» de más abajo.

1. **¿Por qué la distancia por calles es mayor que la línea recta?**  
   _Dónde mirar:_ Mira `construir_grafo_calles`: solo se avanza por calles de la cuadrícula.
2. **¿Cuántas veces se ejecuta Dijkstra para una instancia de n clientes y cuál es su complejidad?**  
   _Dónde mirar:_ `matriz_distancias`: una vez por cada cliente y el almacén (n+1). Cada una es O((V+E) log V).
3. **¿Para qué sirve la cola de prioridad (`heapq`)?**  
   _Dónde mirar:_ `dijkstra`: siempre saca el nodo con menor distancia conocida.

Tu guion de 1 minuto para la exposición está en `docs/PRESENTACION.md` (busca tu rol).

## Mis respuestas
_(Escribe aquí tus respuestas, 2 o 3 líneas por pregunta.)_

1. 
2. 
3. 

## Paso 5. Subir tu trabajo (rama → Pull Request → main)
```bash
git add .
git commit -m "docs(rol03): evidencia y respuestas"
git push -u origin feature/rol03-distancias
```
En GitHub: **Compare & pull request** hacia `main` → completa la plantilla → pide revisión a un compañero → cuando las pruebas (Actions) estén en verde, **Merge pull request**.
Antes de abrir el PR, cambia en el `README.md` **solo tu fila** del tablero: pon tu nombre y ✅. Guía de Git: `docs/GUIA_GIT.md`.

## Lista de verificación
- [ ] Ejecuté el comando del Paso 2 sin errores
- [ ] Guardé los archivos de entrega
- [ ] Escribí mis respuestas
- [ ] Actualicé mi fila del README
- [ ] Abrí el Pull Request y se unió a `main`
