# ROL 9: Página web

La página donde se ven los mapas y la comparación. Tú la abres, la pruebas y tomas las capturas para el informe.

> **El código ya está terminado y probado.** Tu tarea es corta: ejecutar, entender tu parte, guardar la evidencia y poder explicarla.

| | |
|---|---|
| **Tu rama** | `feature/rol09-interfaz-web` |
| **Tu parte en el código** | `app.py y carpeta web/` |
| **Tiempo estimado** | 30–45 minutos |

## Paso 1. Preparar (una sola vez)
```bash
git clone <URL-DEL-REPOSITORIO>
cd ruta-optima-ultima-milla
git checkout feature/rol09-interfaz-web
python -m pip install -r requirements.txt
```
Si Git dice que la rama no existe, créala: `git checkout -b feature/rol09-interfaz-web`.

## Paso 2. Ejecutar
```bash
python app.py
```
Debe terminar sin errores y mostrar resultados en la terminal. Si falla, mira `EJECUTAR.md` (sección «Si algo falla»).

## Paso 3. Qué debes guardar (entrega)
- `docs/capturas/01_comparacion.png`
- `docs/capturas/02_detalle.png`
- `docs/capturas/03_experimentos.png`
- `docs/capturas/04_distritos.png`

## Capturas (para el informe)
1. Con la página abierta, deja los valores por defecto y presiona **Calcular rutas**. Marca «Mostrar las zonas». Captura la pestaña *Comparación* → guarda como `docs/capturas/01_comparacion.png`.
2. Pestaña *Detalle de rutas* → `docs/capturas/02_detalle.png`.
3. Pestaña *Experimentos* → `docs/capturas/03_experimentos.png`.
4. Marca «Clientes agrupados por distritos», pon 80 clientes y calcula → `docs/capturas/04_distritos.png`.

## Personalización (opcional, 2 minutos)
En `web/estilos.css`, arriba, cambia el color `--acento` (ejemplo: `#2457d6` → `#d6246e`) y en `web/index.html` agrega los nombres del equipo en la línea `<span class="etiqueta">`.


## Paso 4. Entiende tu parte (te la van a preguntar)
Abre el archivo indicado, lee los comentarios y responde estas preguntas **con tus palabras** en la sección «Mis respuestas» de más abajo.

1. **¿Cómo se comunican la página y Python?**  
   _Dónde mirar:_ `web/app.js` hace `fetch('/api/resolver')`; `app.py` responde con JSON.
2. **¿Qué hace el botón «Otra instancia»?**  
   _Dónde mirar:_ `web/app.js`: cambia la semilla al azar y vuelve a calcular.
3. **¿Por qué algunos clientes salen en rojo en el mapa?**  
   _Dónde mirar:_ No se pudieron atender dentro de su ventana, la capacidad o la jornada.

Tu guion de 1 minuto para la exposición está en `docs/PRESENTACION.md` (busca tu rol).

## Mis respuestas
_(Escribe aquí tus respuestas, 2 o 3 líneas por pregunta.)_

1. La página web se comunica con Python mediante una solicitud llamada fetch. Cuando presionamos el botón para calcular, JavaScript envía los datos al servidor Python, este ejecuta los algoritmos y devuelve los resultados en formato JSON para mostrarlos en la página.

2. Este botón genera una nueva semilla aleatoria y vuelve a ejecutar el cálculo. De esta manera, podemos obtener diferentes ejemplos de clientes, ubicaciones y rutas para comparar los resultados.

3. Los clientes aparecen en rojo cuando no pudieron ser atendidos por alguna de las estrategias. Esto puede ocurrir porque se supera la capacidad del vehículo, no se llega dentro del horario permitido o se acaba el tiempo de la jornada.

## Paso 5. Subir tu trabajo (rama → Pull Request → main)
```bash
git add .
git commit -m "docs(rol09): evidencia y respuestas"
git push -u origin feature/rol09-interfaz-web
```
En GitHub: **Compare & pull request** hacia `main` → completa la plantilla → pide revisión a un compañero → cuando las pruebas (Actions) estén en verde, **Merge pull request**.
Antes de abrir el PR, cambia en el `README.md` **solo tu fila** del tablero: pon tu nombre y ✅. Guía de Git: `docs/GUIA_GIT.md`.

## Lista de verificación
- [✅ ] Ejecuté el comando del Paso 2 sin errores
- [ ✅] Guardé los archivos de entrega
- [✅ ] Escribí mis respuestas
- [ ] Actualicé mi fila del README
- [ ] Abrí el Pull Request y se unió a `main`
