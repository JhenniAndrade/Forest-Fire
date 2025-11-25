import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.sequencial import simular
from src.paralelo import simular_paralelo_final

def benchmark_threads():
    """Benchmark comparando sequencial vs paralelo com diferentes threads."""
    
    print("\n===== Benchmark: Sequencial vs Paralelo =====\n")
    
    # Configurações de teste
    configuracoes = [
        {"n": 100, "iteracoes": 50},
        {"n": 200, "iteracoes": 50},
        {"n": 400, "iteracoes": 25},
    ]
    
    threads_list = [2, 4, 8]
    
    for config in configuracoes:
        n = config["n"]
        iteracoes = config["iteracoes"]
        
        print(f"Matriz {n}x{n} - {iteracoes} iterações")
        print("-" * 40)
        
        # Sequencial
        tempo_seq = simular(n, iteracoes)
        print(f"Sequencial:\t{tempo_seq:.4f}s")
        
        # Paralelo
        print("Threads\tTempo (s)\tSpeedup")
        for threads in threads_list:
            tempo_par = simular_paralelo(n, iteracoes, threads, "linhas")
            speedup = tempo_seq / tempo_par
            print(f"{threads}\t{tempo_par:.4f}\t\t{speedup:.2f}x")
        
        print()


# Tamanhos de matriz
sizes = [100, 200, 500, 800, 1000]
iterations = 100 

print("\n===== Benchmark da Versão Sequencial =====\n")
print("Matriz\tIterações\tTempo (s)")
print("------------------------------------------")

for n in sizes:
    tempo = simular(n, iterations)
    print(f"{n}x{n}\t{iterations}\t\t{tempo:.4f}")

# Executa também o benchmark de threads
benchmark_threads()
