# ROL 6: Programación dinámica (Held-Karp)

El módulo más importante: encuentra el mejor orden exacto de visita dentro de una zona.

> **El código ya está terminado y probado.** Tu tarea es corta: ejecutar, entender tu parte, guardar la evidencia y poder explicarla.

| | |
|---|---|
| **Tu rama** | `feature/rol06-held-karp` |
| **Tu parte en el código** | `ruta_optima/held_karp.py` |
| **Tiempo estimado** | 30–45 minutos |

## Paso 1. Preparar (una sola vez)
```bash
git clone <URL-DEL-REPOSITORIO>
cd ruta-optima-ultima-milla
git checkout feature/rol06-held-karp
python -m pip install -r requirements.txt
```
Si Git dice que la rama no existe, créala: `git checkout -b feature/rol06-held-karp`.

## Paso 2. Ejecutar
```bash
scripts/rol06_held_karp.py
```
Debe terminar sin errores y mostrar resultados en la terminal. Si falla, mira `EJECUTAR.md` (sección «Si algo falla»).

## Paso 3. Qué debes guardar (entrega)
- `resultados/held_karp_tiempo.png`

## Paso 4. Entiende tu parte (te la van a preguntar)
Abre el archivo indicado, lee los comentarios y responde estas preguntas **con tus palabras** en la sección «Mis respuestas» de más abajo.

1. **¿Qué significa `dp[mascara][j]`?**  
   _Dónde mirar:_ Comentario al inicio de `ordenar_zona` en `ruta_optima/held_karp.py`.
2. **¿Cuál es la complejidad y por qué solo se usa en zonas de k ≤ 12-14 clientes?**  
   _Dónde mirar:_ O(k²·2^k). Mira el gráfico que genera el script: crece muy rápido.
3. **¿Qué hace el código cuando el vehículo llega ANTES de que abra la ventana de un cliente?**  
   _Dónde mirar:_ Busca `max(..., c.ventana_ini)`: espera hasta que abra.

Tu guion de 1 minuto para la exposición está en `docs/PRESENTACION.md` (busca tu rol).

## Mis respuestas
_(Escribe aquí tus respuestas, 2 o 3 líneas por pregunta.)_

1. `dp[mascara][j]` guarda el instante más temprano en que el vehículo puede terminar de atender al cliente `j`, habiendo visitado exactamente los clientes marcados en `mascara`. La máscara es un número cuyos bits encendidos indican qué clientes ya se atendieron. Así cada combinación (subconjunto, último cliente) se calcula una sola vez.
2. La complejidad es O(k²·2^k) en tiempo y O(k·2^k) en memoria: hay 2^k subconjuntos, k posibles últimos clientes y por cada uno se prueban k siguientes. En mi prueba k = 12 tardó ~0.05 s y k = 14 ~0.26 s; cada cliente extra casi duplica el tiempo. Por eso solo se usa en zonas pequeñas (k ≤ 12-14) y no con los 200 clientes juntos.
3. Si llega antes de que abra la ventana, el vehículo espera: el inicio del servicio se calcula como `max(hora_de_llegada, c.ventana_ini)`. Si la hora de inicio pasa de `ventana_fin`, ese orden se descarta porque llegaría tarde.

## Paso 5. Subir tu trabajo (rama → Pull Request → main)
```bash
git add .
git commit -m "docs(rol06): evidencia y respuestas"
git push -u origin feature/rol06-held-karp
```
En GitHub: **Compare & pull request** hacia `main` → completa la plantilla → pide revisión a un compañero → cuando las pruebas (Actions) estén en verde, **Merge pull request**.
Antes de abrir el PR, cambia en el `README.md` **solo tu fila** del tablero: pon tu nombre y ✅. Guía de Git: `docs/GUIA_GIT.md`.

## Lista de verificación
- [x] Ejecuté el comando del Paso 2 sin errores
- [x] Guardé los archivos de entrega
- [x] Escribí mis respuestas
- [x] Actualicé mi fila del README
- [x] Abrí el Pull Request y se unió a `main`
