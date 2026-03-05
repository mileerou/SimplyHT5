"""
HDT5: Simulación de corrida de progmemoria_ramas
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
    (1) NEW -> (se le asigna memoria_ram) -> (2) READY -> (espera al CPU)
     -> (3) RUNNING -> (I/O o espera evento) -> (4) TERMINATED
    """
    llegada = env.now                   # Marca el inicio del env

    # 1. NEW (solicita memoria)
    memoria = random.int (1,10)
    yield memoria_ram.get(memoria)              # Guarda el resultado del memoria_ram (usando la memoria)

    # 2. READY
    instrucciones = random.randint(1, 10)
    while instrucciones > 0:
        with velocidad_cpu.request() as turno:
            yield turno                         # Espera su turno

            # 3. RUNNING
            yield env.timeout(tiempo_cpu)                       # Usa el env por la unidad de tiempo
            ejecutadas = min(velocidad_cpu,instrucciones)       # Consigue el mínimo de instrucciones que sí se realizaron
            instrucciones -= ejecutadas                         # Le resta al total de instrucciones por completar, las que se completaron
        
        # 4. TERMINATED
        if instrucciones == 0:
            break
    
    memoria_ram.put(memoria)
    tiempo_total = env.now - llegada
    tiempo_cpu.append(tiempo_total)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def generador_procesos(env, velocidad_cpu, memoria_ram, numero_procesos, tiempo_cpu):    #sistema que envía procesos a la CPU y memoria_ram
    for i in range(numero_procesos):
        env.process(proceso(env, f'Proceso {i}', velocidad_cpu, memoria_ram, tiempo_cpu))
        intervalo = random.expovariate(1.0 / sp.Interval)
        yield env.timeout(intervalo)

def simulacion(numero_procesos):
    random.seed(random_seed)
    env = sp.Environment()
    velocidad_cpu = sp.Resource(env, velocidad_cpu)
    memoria_ram = sp.Container(env, init=sp.memoria_ramcapacity, capacity=sp.memoria_ramcapacity)
    tiempo_cpu = []
    
    env.process(generador_procesos(env, velocidad_cpu, memoria_ram, numero_procesos, tiempo_cpu))
    env.run()
    return tiempo_cpu

casos = [25, 50, 100, 150, 200]
promedios = []
desv_std = []

print(f"{'Procesos':>10} {'Promedio':>12} {'Desv. Std':>12}")
print("-" * 38)

for n in casos:
    tiempo_cpu = simulacion(n)
    media = statistics.mean(tiempo_cpu)
    std = statistics.stdev(tiempo_cpu) if len(tiempo_cpu) > 1 else 0
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


# FIN DE PROGmemoria_ramA
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~