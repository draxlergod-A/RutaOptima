# ROL 5: Estrategia voraz y reparto de zonas

El módulo de la Estrategia 1 (vecino más cercano) y del reparto equilibrado de zonas a vehículos.

> **El código ya está terminado y probado.** Tu tarea es corta: ejecutar, entender tu parte, guardar la evidencia y poder explicarla.

| | |
|---|---|
| **Tu rama** | `feature/rol05-voraz` |
| **Tu parte en el código** | `ruta_optima/voraz.py` |
| **Tiempo estimado** | 30–45 minutos |

## Paso 1. Preparar (una sola vez)
```bash
git clone <URL-DEL-REPOSITORIO>
cd ruta-optima-ultima-milla
git checkout feature/rol05-voraz
python -m pip install -r requirements.txt
```
Si Git dice que la rama no existe, créala: `git checkout -b feature/rol05-voraz`.

## Paso 2. Ejecutar
```bash
scripts/rol05_voraz.py
```
Debe terminar sin errores y mostrar resultados en la terminal. Si falla, mira `EJECUTAR.md` (sección «Si algo falla»).

## Paso 3. Qué debes guardar (entrega)
- `resultados/atendidos_vs_vehiculos.png`

## Paso 4. Entiende tu parte (te la van a preguntar)
Abre el archivo indicado, lee los comentarios y responde estas preguntas **con tus palabras** en la sección «Mis respuestas» de más abajo.

1. **¿Cómo decide `ruta_voraz` a qué cliente ir después?**  
   _Dónde mirar:_ `ruta_voraz`: el más cercano que sea factible (`evaluar_orden`).
2. **¿Por qué `asignar_zonas` reparte el trabajo entre vehículos en vez de llenar cada vehículo hasta 100 de capacidad?**  
   _Dónde mirar:_ Lee el docstring de `asignar_zonas`: el límite real es el tiempo de la jornada.
3. **Da un ejemplo de por qué un algoritmo voraz no siempre da la mejor ruta.**  
   _Dónde mirar:_ Mira un mapa de la página: el voraz deja clientes lejanos para el final.

Tu guion de 1 minuto para la exposición está en `docs/PRESENTACION.md` (busca tu rol).

## Mis respuestas
_(Escribe aquí tus respuestas, 2 o 3 líneas por pregunta.)_

1. 
2. 
3. 

## Paso 5. Subir tu trabajo (rama → Pull Request → main)
```bash
git add .
git commit -m "docs(rol05): evidencia y respuestas"
git push -u origin feature/rol05-voraz
```
En GitHub: **Compare & pull request** hacia `main` → completa la plantilla → pide revisión a un compañero → cuando las pruebas (Actions) estén en verde, **Merge pull request**.
Antes de abrir el PR, cambia en el `README.md` **solo tu fila** del tablero: pon tu nombre y ✅. Guía de Git: `docs/GUIA_GIT.md`.

## Lista de verificación
- [ ] Ejecuté el comando del Paso 2 sin errores
- [ ] Guardé los archivos de entrega
- [ ] Escribí mis respuestas
- [ ] Actualicé mi fila del README
- [ ] Abrí el Pull Request y se unió a `main`
