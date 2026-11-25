# ROL 2: Instancias de prueba (guardar y cargar)

El módulo que guarda un problema en un archivo para poder repetir el experimento exacto.

> **El código ya está terminado y probado.** Tu tarea es corta: ejecutar, entender tu parte, guardar la evidencia y poder explicarla.

| | |
|---|---|
| **Tu rama** | `feature/rol02-instancias` |
| **Tu parte en el código** | `ruta_optima/instancias.py` |
| **Tiempo estimado** | 30–45 minutos |

## Paso 1. Preparar (una sola vez)
```bash
git clone <URL-DEL-REPOSITORIO>
cd ruta-optima-ultima-milla
git checkout feature/rol02-instancias
python -m pip install -r requirements.txt
```
Si Git dice que la rama no existe, créala: `git checkout -b feature/rol02-instancias`.

## Paso 2. Ejecutar
```bash
scripts/rol02_instancias.py
```
Debe terminar sin errores y mostrar resultados en la terminal. Si falla, mira `EJECUTAR.md` (sección «Si algo falla»).

## Paso 3. Qué debes guardar (entrega)
- `resultados/instancias/pequena.json`
- `resultados/instancias/mediana.json`
- `resultados/instancias/grande.json`

## Paso 4. Entiende tu parte (te la van a preguntar)
Abre el archivo indicado, lee los comentarios y responde estas preguntas **con tus palabras** en la sección «Mis respuestas» de más abajo.

1. **¿Qué pasa si generas dos veces una instancia con la misma semilla? ¿Dónde se ve en el código?**  
   _Dónde mirar:_ `ruta_optima/generador.py`, busca `random.Random(semilla)`.
2. **¿Para qué sirve guardar la instancia en un JSON?**  
   _Dónde mirar:_ `guardar_instancia` y `cargar_instancia` en `ruta_optima/instancias.py`.
3. **¿Qué cambia en `generar_instancia_distritos` respecto a `generar_instancia`?**  
   _Dónde mirar:_ Mira `ruta_optima/instancias.py`: solo cambian las coordenadas (`random.gauss`).

Tu guion de 1 minuto para la exposición está en `docs/PRESENTACION.md` (busca tu rol).

## Mis respuestas
_(Escribe aquí tus respuestas, 2 o 3 líneas por pregunta.)_

1. 
2. 
3. 

## Paso 5. Subir tu trabajo (rama → Pull Request → main)
```bash
git add .
git commit -m "docs(rol02): evidencia y respuestas"
git push -u origin feature/rol02-instancias
```
En GitHub: **Compare & pull request** hacia `main` → completa la plantilla → pide revisión a un compañero → cuando las pruebas (Actions) estén en verde, **Merge pull request**.
Antes de abrir el PR, cambia en el `README.md` **solo tu fila** del tablero: pon tu nombre y ✅. Guía de Git: `docs/GUIA_GIT.md`.

## Lista de verificación
- [ ] Ejecuté el comando del Paso 2 sin errores
- [ ] Guardé los archivos de entrega
- [ ] Escribí mis respuestas
- [ ] Actualicé mi fila del README
- [ ] Abrí el Pull Request y se unió a `main`
