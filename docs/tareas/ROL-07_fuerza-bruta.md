# ROL 7: Fuerza bruta (verificador)

El módulo que prueba todos los órdenes posibles para comprobar que Held-Karp sí encuentra el óptimo.

> **El código ya está terminado y probado.** Tu tarea es corta: ejecutar, entender tu parte, guardar la evidencia y poder explicarla.

| | |
|---|---|
| **Tu rama** | `feature/rol07-fuerza-bruta` |
| **Tu parte en el código** | `ruta_optima/fuerza_bruta.py` |
| **Tiempo estimado** | 30–45 minutos |

## Paso 1. Preparar (una sola vez)
```bash
git clone <URL-DEL-REPOSITORIO>
cd ruta-optima-ultima-milla
git checkout feature/rol07-fuerza-bruta
python -m pip install -r requirements.txt
```
Si Git dice que la rama no existe, créala: `git checkout -b feature/rol07-fuerza-bruta`.

## Paso 2. Ejecutar
```bash
scripts/rol07_verificacion.py
```
Debe terminar sin errores y mostrar resultados en la terminal. Si falla, mira `EJECUTAR.md` (sección «Si algo falla»).

## Paso 3. Qué debes guardar (entrega)
- `resultados/fuerza_bruta_vs_held_karp.png`

## Paso 4. Entiende tu parte (te la van a preguntar)
Abre el archivo indicado, lee los comentarios y responde estas preguntas **con tus palabras** en la sección «Mis respuestas» de más abajo.

1. **¿Por qué necesitamos un algoritmo lento si ya tenemos Held-Karp?**  
   _Dónde mirar:_ Sirve de referencia: si dos métodos distintos dan lo mismo, hay confianza en que ambos son correctos.
2. **Mira la salida del script: ¿en cuántas zonas coinciden? ¿Cuánto tarda cada uno con k = 9?**  
   _Dónde mirar:_ El script imprime ambos resultados.
3. **Complejidad de la fuerza bruta vs Held-Karp.**  
   _Dónde mirar:_ O(k!) vs O(k²·2^k).

Tu guion de 1 minuto para la exposición está en `docs/PRESENTACION.md` (busca tu rol).

## Mis respuestas

1. Held-Karp es rápido, pero tiene más lógica y es más fácil equivocarse. La fuerza bruta es simple porque prueba todos los órdenes, así que sirve de referencia: si ambos dan el mismo resultado, podemos confiar en Held-Karp.
2. Coinciden en 200 de 200 zonas al azar (el mismo instante final, o ambos sin solución). Con k = 9, en mi ejecución la fuerza bruta tardó 0.90 s y Held-Karp 0.004 s.
3. La fuerza bruta es O(k!) órdenes (O(k·k!) si se cuenta el recorrido de cada uno) y Held-Karp es O(k²·2^k). El factorial crece mucho más rápido: de k = 8 a k = 9 la fuerza bruta tardó unas 9 veces más y Held-Karp unas 2.3 veces más.

## Paso 5. Subir tu trabajo (rama → Pull Request → main)
```bash
git add .
git commit -m "docs(rol07): evidencia y respuestas"
git push -u origin feature/rol07-fuerza-bruta
```
En GitHub: **Compare & pull request** hacia `main` → completa la plantilla → pide revisión a un compañero → cuando las pruebas (Actions) estén en verde, **Merge pull request**.
Antes de abrir el PR, cambia en el `README.md` **solo tu fila** del tablero: pon tu nombre y ✅. Guía de Git: `docs/GUIA_GIT.md`.

## Lista de verificación
- [x] Ejecuté el comando del Paso 2 sin errores
- [x] Guardé los archivos de entrega
- [x] Escribí mis respuestas
- [x] Actualicé mi fila del README
- [x] Abrí el Pull Request y se unió a `main`
