"""Parámetros del caso simulado.

Son los mismos valores de la Tabla 1 del informe técnico.
IMPORTANTE: si cambias un valor aquí, avisa al equipo para cambiarlo también en el informe.

Unidades que se usan en TODO el proyecto:
  - tiempo ........ minutos desde las 00:00 (09:00 = 540)
  - distancia ..... kilómetros
  - dinero ........ soles (S/)
"""

# ---- Vehículos y jornada -------------------------------------------------
CAPACIDAD = 100                 # paquetes por vehículo (Q)
JORNADA_MAX_MIN = 8 * 60        # jornada máxima de una ruta: 8 horas
HORA_SALIDA_MIN = 9 * 60        # todos los vehículos salen del almacén a las 09:00
FLOTA_MAX = 15                  # máximo de vehículos (m)

# ---- Clientes ------------------------------------------------------------
N_MIN = 20                      # tamaño mínimo del caso del proyecto
N_MAX = 200                     # tamaño máximo del caso del proyecto
DEMANDA_RANGO = (1, 6)          # paquetes por cliente (mínimo, máximo)
SERVICIO_RANGO_MIN = (5, 10)    # minutos de servicio por cliente
VENTANA_DURACION_MIN = 120      # cada ventana dura 2 horas
VENTANA_INICIO_MIN = 9 * 60     # primera ventana posible: empieza a las 09:00
VENTANA_INICIO_MAX = 16 * 60    # última ventana posible: empieza a las 16:00 (termina 18:00)
VENTANA_PASO_MIN = 30           # las ventanas empiezan en múltiplos de 30 minutos

# ---- Ciudad simulada -----------------------------------------------------
AREA_KM = 20.0                  # la ciudad es un cuadrado de 20 x 20 km
VELOCIDAD_KMH = 25.0            # velocidad media urbana (tráfico de Lima)
FACTOR_VIAL = 1.3               # una calle real es ~30 % más larga que la línea recta

# ---- Costos (función objetivo) ------------------------------------------
COSTO_KM = 1.20                 # S/ por km recorrido
COSTO_HORA = 12.50              # S/ por hora de operación

# ---- Algoritmos ------------------------------------------------------------
K_ZONA = 12                     # máximo de clientes por zona (Held-Karp cuesta ~ k^2 * 2^k)
SEMILLA_DEFECTO = 42            # semilla del generador aleatorio (resultados repetibles)

# Tolerancia numérica para comparar números decimales
EPS = 1e-9
