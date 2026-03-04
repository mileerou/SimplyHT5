"""
HDT5: Simulación de corrida de programas
Yu-Fong Chen (242115) y Milena Rodriguez (251027)
"""

import sympy
import random
import statistics
import matplotlib.pyplot as plt         # Para hacer las gráficas

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Parámetros modificables
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

random_seed = 64                        # Semilla para generar la misma secuencia
memoria_ram = 100                       # Memoria total
velocidad_cpu = 3                       # Instrucciones por unidad de tiempo
tiempo_cpu = 1                          # Unidad de tiempo
intervalo = 10                          # Intervalo promedio entre llegadas

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def proceso ():
    """
    (1) NEW -> (se le asigna RAM) -> (2) READY -> (espera al CPU)
     -> (3) RUNNING -> (I/O o espera evento) -> (4) TERMINATED
    """
    llegada = env.now                   # Marca el inicio del env

    # 1. NEW (solicita memoria)
    memoria = random.int (1,10)
    yield ram.get(memoria)              # Guarda el resultado del ram (usando la memoria)

    # 2. READY
    instrucciones = random.randint(1, 10)
    while instrucciones > 0:
        with cpu.request() as turno:
            yield turno                         # Espera su turno

            # 3. RUNNING
            yield env.timeout(tiempo_cpu)                       # Usa el env por la unidad de tiempo
            ejecutadas = min(velocidad_cpu,instrucciones)       # Consigue el mínimo de instrucciones que sí se realizaron
            instrucciones -= ejecutadas                         # Le resta al total de instrucciones por completar, las que se completaron
        
        # 4. TERMINATED
        if instrucciones == 0:
            break
    
    ram.put(memoria)
    tiempo_total = env.now - llegada
    tiempos.append(tiempo_total)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




# FIN DE PROGRAMA
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~