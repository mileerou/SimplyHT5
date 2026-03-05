"""
HDT5: Simulación de corrida de programas
Yu-Fong Chen (242115) y Milena Rodriguez (251027)
"""

import simpy as sim
import random
import statistics
import matplotlib.pyplot as plt         # Para hacer las gráficas

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Parámetros modificables
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

random_seed = 64                        # Semilla para generar la misma secuencia
memoria_ram = 100                       # Memoria total disponible en RAM
velocidad_cpu = 3                       # instrucciones por unidad de tiempo
unidad_tiempo = 1                      # duración de la unidad de tiempo de CPU
intervalo = 10                          # intervalo promedio entre llegadas

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def proceso(env, nombre, cpu, ram, tiempos):
    """Ciclo de vida de un proceso en el sistema."""
    llegada = env.now
    memoria = random.randint(1, 10)
    yield ram.get(memoria)
    instrucciones = random.randint(1, 10)
    while instrucciones > 0:
        with cpu.request() as turno:
            yield turno
            yield env.timeout(unidad_tiempo)
            ejecutadas = min(velocidad_cpu, instrucciones)
            instrucciones -= ejecutadas
        if instrucciones == 0:
            break
    ram.put(memoria)
    tiempos.append(env.now - llegada)


def generador_procesos(env, cpu, ram, numero_procesos, tiempos):
    for i in range(numero_procesos):
        env.process(proceso(env, f"Proceso {i}", cpu, ram, tiempos))
        intervalo_siguiente = random.expovariate(1.0 / intervalo)
        yield env.timeout(intervalo_siguiente)


def simulacion(numero_procesos):
    random.seed(random_seed)
    env = sim.Environment()
    cpu = sim.Resource(env, capacity=1)
    ram = sim.Container(env, init=memoria_ram, capacity=memoria_ram)
    tiempos = []
    env.process(generador_procesos(env, cpu, ram, numero_procesos, tiempos))
    env.run()
    return tiempos


if __name__ == "__main__":
    casos = [25, 50, 100, 150, 200]
    promedios = []
    desv_std = []
    print(f"{'Procesos':>10} {'Promedio':>12} {'Desv. Std':>12}")
    print("-" * 38)
    for n in casos:
        tiempos_res = simulacion(n)
        media = statistics.mean(tiempos_res)
        std = statistics.stdev(tiempos_res) if len(tiempos_res) > 1 else 0
        promedios.append(media)
        desv_std.append(std)
        print(f"{n:>10} {media:>12.2f} {std:>12.2f}")

    
    fig, ax = plt.subplots(figsize=(8, 5))
    
    ax.errorbar(casos, promedios, yerr=desv_std, marker='o', linewidth=2, capsize=5, color='lavenderblush', ecolor='orchid', label='Tiempo promedio ± desv. std')
    ax.set_xlabel("Número de procesos", fontsize=12)
    ax.set_ylabel("Tiempo promedio en el sistema", fontsize=12)
    ax.set_title("Tiempo promedio en el sistema vs Número de procesos", fontsize=14)
    ax.set_xticks(casos)
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()
