#!/usr/bin/env bash
# Crea en GitHub las ramas de trabajo de cada rol (ejecutar UNA vez, el coordinador, en la carpeta del repo).
set -e
for rama in \
  feature/rol02-instancias \
  feature/rol03-distancias \
  feature/rol04-zonas \
  feature/rol05-voraz \
  feature/rol06-held-karp \
  feature/rol07-fuerza-bruta \
  feature/rol08-benchmark-pruebas \
  feature/rol09-interfaz-web \
  feature/rol10-informe-y-sustentacion
do
  git branch "$rama" main
  git push -u origin "$rama"
done
git checkout main
echo "Listo: ramas creadas."
