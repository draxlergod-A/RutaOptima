# Guía de Git y GitHub para el equipo

Modelo: una rama `main` (siempre funcionando) y **una rama por rol**. Cada rol termina su parte, abre un **Pull Request (PR)** y se une a `main`.

```
main ──●─────────────●────────●────────────●──  (siempre estable)
        \           /          \          /
         rol04-zonas             rol06-held-karp
```

| Rol | Rama |
|---|---|
| 2 | `feature/rol02-instancias` |
| 3 | `feature/rol03-distancias` |
| 4 | `feature/rol04-zonas` |
| 5 | `feature/rol05-voraz` |
| 6 | `feature/rol06-held-karp` |
| 7 | `feature/rol07-fuerza-bruta` |
| 8 | `feature/rol08-benchmark-pruebas` |
| 9 | `feature/rol09-interfaz-web` |
| 10 | `feature/rol10-informe-y-sustentacion` |

---

## A. Coordinador (ROL 1) — se hace UNA vez

1. Crea en GitHub un repositorio **vacío** llamado `ruta-optima-ultima-milla` (sin README ni .gitignore, para evitar conflictos).
2. Descomprime el `.zip` y, dentro de la carpeta, ejecuta:

```bash
git init -b main
git add .
git commit -m "feat(base): proyecto base con modelos, evaluador, solver, pruebas y guías"
git remote add origin https://github.com/TU-USUARIO/ruta-optima-ultima-milla.git
git push -u origin main
```

3. Verifica que en GitHub aparezca la pestaña **Actions** con la prueba `tests` en verde.
4. **Crea las ramas de los roles** (elige una opción):

```bash
# Linux / Mac / Git Bash
bash scripts/crear_ramas.sh
```
```powershell
# Windows PowerShell
./scripts/crear_ramas.ps1
```
(Si PowerShell bloquea el script: `Set-ExecutionPolicy -Scope Process Bypass`.)

5. Invita a los 9 compañeros: **Settings → Collaborators → Add people**.
6. Protege `main`: **Settings → Branches → Add branch ruleset** (o *Add rule*) para `main`:
   - ✔ Require a pull request before merging (1 aprobación)
   - ✔ Require status checks to pass → elige `pytest`
   - ✔ Block force pushes
7. Escribe en el README el nombre de cada responsable y manda a cada uno el enlace a su guía `docs/tareas/ROL-XX_...md`.

---

## B. Cada integrante (ROLES 2 a 10)

**1. Clonar (solo la primera vez)**
```bash
git clone https://github.com/TU-USUARIO/ruta-optima-ultima-milla.git
cd ruta-optima-ultima-milla
pip install -r requirements.txt
```

**2. Ir a tu rama** (cambia el nombre por el tuyo)
```bash
git checkout feature/rol04-zonas
git pull origin main        # trae lo último de main a tu rama
```

**3. Trabajar.** Abre tu guía `docs/tareas/ROL-XX_...md` y sigue los pasos (ejecutar, guardar evidencia, responder preguntas). Comandos útiles:
```bash
python -m pytest tests/test_zonas.py -v     # solo tus pruebas
python -m pytest                            # todas
python main.py --estado                     # tablero
```

**4. Guardar tu avance** (puedes hacerlo varias veces al día)
```bash
git add .
git commit -m "docs(rol04): evidencia y respuestas"
git push -u origin feature/rol04-zonas
```

**5. Pull Request** (cuando termines y tus pruebas pasen)
1. En GitHub verás el botón **Compare & pull request** → base: `main`, compare: tu rama.
2. Completa la plantilla (lista de verificación) y en *Reviewers* elige a un compañero.
3. Espera a que **Actions** esté en verde ✔ y que el revisor apruebe.
4. Haz clic en **Merge pull request** → *Confirm*.
5. Actualiza la fila de tu rol en el README (si no lo hiciste antes del PR).

**6. Después del merge**
```bash
git checkout main
git pull origin main
```

### Formato de mensajes de commit
`tipo(rolNN): qué hiciste` — tipos: `feat` (algo nuevo), `fix` (corregir), `test` (pruebas), `docs` (documentación).
Ejemplos: `feat(rol06): held-karp con ventanas de tiempo`, `fix(rol04): empates en la mediana`.

---

## C. Problemas frecuentes

**Conflicto al hacer `git pull origin main`.** Git marca el archivo con `<<<<<<<`, `=======`, `>>>>>>>`. Abre el archivo, deja la versión correcta (borra las marcas), y luego:
```bash
git add archivo.py
git commit -m "fix: resolver conflicto"
```
Como cada rol toca su propio archivo, los conflictos solo deberían aparecer en el **README (tu fila)**. Cambia solo tu fila.

**«Me equivoqué de rama».** Si aún no hiciste commit: `git stash`, `git checkout rama-correcta`, `git stash pop`.

**«Falla Actions pero en mi PC pasa».** Corre `python -m pytest` desde la carpeta raíz del repo y verifica que no dependes de archivos que no subiste (`git status`).

**«Necesito algo de otro rol que aún no está en main».** Usa las matrices aproximadas (ver `docs/ARQUITECTURA.md`) o espera su merge y haz `git pull origin main`.

**Alternativa sin Pull Requests** (si el equipo prefiere algo más simple; el PR es lo recomendado):
```bash
git checkout main
git pull origin main
git merge feature/rol04-zonas
python -m pytest
git push origin main
```
