# ROL 10: Informe final y sustentación

Une todo: completa el informe con los resultados reales y organiza la exposición del equipo.

> **El código ya está terminado y probado.** Tu tarea es corta: ejecutar, entender tu parte, guardar la evidencia y poder explicarla.

| | |
|---|---|
| **Tu rama** | `feature/rol10-informe-y-sustentacion` |
| **Tu parte en el código** | `docs/PRESENTACION.md + informe Word` |
| **Tiempo estimado** | 30–45 minutos |

## Paso 1. Preparar (una sola vez)
```bash
git clone <URL-DEL-REPOSITORIO>
cd ruta-optima-ultima-milla
git checkout feature/rol10-informe-y-sustentacion
python -m pip install -r requirements.txt
```
Si Git dice que la rama no existe, créala: `git checkout -b feature/rol10-informe-y-sustentacion`.

## Paso 2. Ejecutar
```bash
python main.py --n 60
```
Debe terminar sin errores y mostrar resultados en la terminal. Si falla, mira `EJECUTAR.md` (sección «Si algo falla»).

## Paso 3. Qué debes guardar (entrega)
- `docs/PRESENTACION.md (orden de exposición completado)`
- `informe Word con resultados`

## Qué debes completar
1. `docs/PRESENTACION.md`: escribe en la tabla «Orden de exposición» el nombre de cada integrante.
2. Informe Word: copia la tabla de `docs/RESULTADOS.md` y los gráficos de `resultados/` en las secciones de resultados; pega las capturas de `docs/capturas/` (las manda el ROL 9).
3. Completa las partes de evaluación final (resumen, abstract, conclusiones) con las conclusiones del ROL 8.
4. Cuando todos los PR estén unidos: en GitHub → **Releases → Create a new release** → etiqueta `v1.0`.


## Paso 4. Entiende tu parte (te la van a preguntar)
Abre el archivo indicado, lee los comentarios y responde estas preguntas **con tus palabras** en la sección «Mis respuestas» de más abajo.

1. **¿Qué tabla y qué gráfico del informe salen de `resultados/`?**  
   _Dónde mirar:_ `resultados/resultados.csv` y los `.png`; `docs/RESULTADOS.md` tiene la tabla lista.
2. **¿Qué parámetros del informe (Tabla 1) están en el código?**  
   _Dónde mirar:_ `ruta_optima/config.py`.
3. **Lista 3 limitaciones del modelo.**  
   _Dónde mirar:_ Ejemplos: calles simuladas, sin tráfico, un solo almacén, velocidad constante.

Tu guion de 1 minuto para la exposición está en `docs/PRESENTACION.md` (busca tu rol).

## Mis respuestas
_(Escribe aquí tus respuestas, 2 o 3 líneas por pregunta.)_

1. 
2. 
3. 

## Paso 5. Subir tu trabajo (rama → Pull Request → main)
```bash
git add .
git commit -m "docs(rol10): evidencia y respuestas"
git push -u origin feature/rol10-informe-y-sustentacion
```
En GitHub: **Compare & pull request** hacia `main` → completa la plantilla → pide revisión a un compañero → cuando las pruebas (Actions) estén en verde, **Merge pull request**.
Antes de abrir el PR, cambia en el `README.md` **solo tu fila** del tablero: pon tu nombre y ✅. Guía de Git: `docs/GUIA_GIT.md`.

## Lista de verificación
- [ ] Ejecuté el comando del Paso 2 sin errores
- [ ] Guardé los archivos de entrega
- [ ] Escribí mis respuestas
- [ ] Actualicé mi fila del README
- [ ] Abrí el Pull Request y se unió a `main`
