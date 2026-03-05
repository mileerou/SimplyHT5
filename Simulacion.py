"""
HDT5: Simulación de corrida de programas
Yu-Fong Chen (242115) y Milena Rodriguez (251027)
"""

import sympy as sp
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

def generador_procesos(env, cpu, ram, numero_procesos, tiempos):    #sistema que envía procesos a la CPU y Ram
    for i in range(numero_procesos):
        env.process(proceso(env, f'Proceso {i}', cpu, ram, tiempos))
        intervalo = random.expovariate(1.0 / sp.Interval)
        yield env.timeout(intervalo)

def simulacion(numero_procesos):
    random.seed(sp.Randomseed)
    env = sp.Environment()
    cpu = sp.Resource(env, velocidad_cpu)
    ram = sp.Container(env, init=sp.RAMcapacity, capacity=sp.RAMcapacity)
    tiempos = []
    
    env.process(generador_procesos(env, cpu, ram, numero_procesos, tiempos))
    env.run()
    return tiempos

casos = [25, 50, 100, 150, 200]
promedios = []
desv_std = []

print(f"{'Procesos':>10} {'Promedio':>12} {'Desv. Std':>12}")
print("-" * 38)

for n in casos:
    tiempos = simulacion(n)
    media = statistics.mean(tiempos)
    std = statistics.stdev(tiempos) if len(tiempos) > 1 else 0
    promedios.append(media)
    desv_std.append(std)
    print(f"{n:>10} {media:>12.2f} {std:>12.2f}")

#Gráficas

fig, ax = plt.subplots(figsize=(8, 5))

ax.errorbar(
    casos, promedios,
    yerr=desv_std,
    marker='o', linewidth=2, capsize=5,
    color = 'lavenderblush', ecolor= 'orchid', label='Tiempo promedio ± desv. std'
)

ax.set_xlabel("Número de procesos", fontsize=12)
ax.set_ylabel("Tiempo promedio en el sistema", fontsize=12)
ax.set_title("Tiempo promedio en el sistema vs Número de procesos", fontsize=14)
ax.set_xticks(casos)
ax.legend()
ax.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()


# FIN DE PROGRAMA
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~