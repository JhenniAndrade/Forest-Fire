from src.sequencial import simular

# Tamanhos de matriz
sizes = [100, 200, 500, 800, 1000]
iterations = 100 

print("\n===== Benchmark da Versão Sequencial =====\n")
print("Matriz\tIterações\tTempo (s)")
print("------------------------------------------")

for n in sizes:
    tempo = simular(n, iterations)
    print(f"{n}x{n}\t{iterations}\t\t{tempo:.4f}")
