# Crea en GitHub las ramas de trabajo de cada rol (ejecutar UNA vez, el coordinador, en la carpeta del repo).
$ramas = @(
  "feature/rol02-instancias",
  "feature/rol03-distancias",
  "feature/rol04-zonas",
  "feature/rol05-voraz",
  "feature/rol06-held-karp",
  "feature/rol07-fuerza-bruta",
  "feature/rol08-benchmark-pruebas",
  "feature/rol09-interfaz-web",
  "feature/rol10-informe-y-sustentacion"
)
foreach ($r in $ramas) {
  git branch $r main
  git push -u origin $r
}
git checkout main
Write-Host "Listo: ramas creadas."
