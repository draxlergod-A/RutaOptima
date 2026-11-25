"""ROL 2: guarda las 3 instancias oficiales en resultados/instancias/ y comprueba que se pueden recargar."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from ruta_optima.instancias import cargar_instancia, guardar_instancia, instancias_de_prueba

os.makedirs("resultados/instancias", exist_ok=True)
for nombre, inst in instancias_de_prueba().items():
    ruta = f"resultados/instancias/{nombre}.json"
    guardar_instancia(inst, ruta)
    igual = cargar_instancia(ruta) == inst
    print(f"{nombre:8s} n={inst.n:3d} vehículos={inst.num_vehiculos:2d}  guardada en {ruta}  recarga idéntica: {igual}")
