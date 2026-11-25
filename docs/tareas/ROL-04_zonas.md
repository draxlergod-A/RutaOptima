# ROL 4: Zonas con divide y vencerás (Quickselect)

El módulo que parte la ciudad en zonas pequeñas cortando por la mediana, de forma recursiva.

> **El código ya está terminado y probado.** Tu tarea es corta: ejecutar, entender tu parte, guardar la evidencia y poder explicarla.

| | |
|---|---|
| **Tu rama** | `feature/rol04-zonas` |
| **Tu parte en el código** | `ruta_optima/zonas.py` |
| **Tiempo estimado** | 30–45 minutos |

## Paso 1. Preparar (una sola vez)
```bash
git clone <URL-DEL-REPOSITORIO>
cd ruta-optima-ultima-milla
git checkout feature/rol04-zonas
python -m pip install -r requirements.txt
```
Si Git dice que la rama no existe, créala: `git checkout -b feature/rol04-zonas`.

## Paso 2. Ejecutar
```bash
scripts/rol04_zonas.py
```
Debe terminar sin errores y mostrar resultados en la terminal. Si falla, mira `EJECUTAR.md` (sección «Si algo falla»).

## Paso 3. Qué debes guardar (entrega)
- `resultados/zonas_k12.png`
- `resultados/zonas_k6.png`

## Paso 4. Entiende tu parte (te la van a preguntar)
Abre el archivo indicado, lee los comentarios y responde estas preguntas **con tus palabras** en la sección «Mis respuestas» de más abajo.

1. **¿Qué hace Quickselect y cuál es su complejidad promedio?**  
   _Dónde mirar:_ `quickselect` en `ruta_optima/zonas.py`: O(n) en promedio.
2. **¿Por qué cortar por la mediana garantiza que las zonas tengan a lo sumo k clientes?**  
   _Dónde mirar:_ `dividir_en_zonas`: cada corte deja mitades iguales; se repite hasta tener k o menos.
3. **Escribe la recurrencia T(n) = 2T(n/2) + O(n). ¿A qué complejidad lleva?**  
   _Dónde mirar:_ Teorema maestro: O(n log n).

Tu guion de 1 minuto para la exposición está en `docs/PRESENTACION.md` (busca tu rol).

## Mis respuestas
_(Escribe aquí tus respuestas, 2 o 3 líneas por pregunta.)_

1. 
2. 
3. 

## Paso 5. Subir tu trabajo (rama → Pull Request → main)
```bash
git add .
git commit -m "docs(rol04): evidencia y respuestas"
git push -u origin feature/rol04-zonas
```
En GitHub: **Compare & pull request** hacia `main` → completa la plantilla → pide revisión a un compañero → cuando las pruebas (Actions) estén en verde, **Merge pull request**.
Antes de abrir el PR, cambia en el `README.md` **solo tu fila** del tablero: pon tu nombre y ✅. Guía de Git: `docs/GUIA_GIT.md`.

## Lista de verificación
- [ ] Ejecuté el comando del Paso 2 sin errores
- [ ] Guardé los archivos de entrega
- [ ] Escribí mis respuestas
- [ ] Actualicé mi fila del README
- [ ] Abrí el Pull Request y se unió a `main`
