import random
import time
import threading
from concurrent.futures import ThreadPoolExecutor

# Estados possíveis
VAZIO = 0
ARVORE = 1
FOGO = 2


def criar_matriz(n, prob_arvore=0.6):
    """Cria uma matriz nxn com árvores distribuídas aleatoriamente."""
    return [
        [ARVORE if random.random() < prob_arvore else VAZIO for _ in range(n)]
        for _ in range(n)
    ]


def contar_vizinhos_fogo(matriz, i, j):
    """Conta vizinhos em chamas de forma otimizada."""
    n = len(matriz)
    count = 0
    
    # Verifica apenas vizinhos válidos
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < n and matriz[ni][nj] == FOGO:
                count += 1
    
    return count


def processar_chunk_otimizado(args):
    """Processa um chunk de células de forma otimizada."""
    matriz, coordenadas, prob_crescimento, prob_fogo = args
    resultados = {}
    
    for i, j in coordenadas:
        cel = matriz[i][j]
        
        if cel == VAZIO:
            novo_estado = ARVORE if random.random() < prob_crescimento else VAZIO
        elif cel == ARVORE:
            if random.random() < prob_fogo or contar_vizinhos_fogo(matriz, i, j) > 0:
                novo_estado = FOGO
            else:
                novo_estado = ARVORE
        else:  # FOGO
            novo_estado = VAZIO
        
        resultados[(i, j)] = novo_estado
    
    return resultados


def proximo_estado_paralelo_otimizado(matriz, num_threads=4, prob_crescimento=0.01, prob_fogo=0.0001):
    """Versão paralela otimizada usando chunks de células."""
    n = len(matriz)
    
    # Gera todas as coordenadas
    todas_coords = [(i, j) for i in range(n) for j in range(n)]
    
    # Divide em chunks
    chunk_size = len(todas_coords) // num_threads
    if chunk_size < 100:  # Chunk muito pequeno, use sequencial
        nova = [[VAZIO for _ in range(n)] for _ in range(n)]
        for i, j in todas_coords:
            cel = matriz[i][j]
            if cel == VAZIO:
                nova[i][j] = ARVORE if random.random() < prob_crescimento else VAZIO
            elif cel == ARVORE:
                if random.random() < prob_fogo or contar_vizinhos_fogo(matriz, i, j) > 0:
                    nova[i][j] = FOGO
                else:
                    nova[i][j] = ARVORE
            else:
                nova[i][j] = VAZIO
        return nova
    
    chunks = []
    for i in range(num_threads):
        inicio = i * chunk_size
        if i == num_threads - 1:
            fim = len(todas_coords)
        else:
            fim = (i + 1) * chunk_size
        
        chunk_coords = todas_coords[inicio:fim]
        chunks.append((matriz, chunk_coords, prob_crescimento, prob_fogo))
    
    # Processa em paralelo
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        resultados_chunks = list(executor.map(processar_chunk_otimizado, chunks))
    
    # Reconstroi matriz
    nova = [[VAZIO for _ in range(n)] for _ in range(n)]
    for resultado_chunk in resultados_chunks:
        for (i, j), valor in resultado_chunk.items():
            nova[i][j] = valor
    
    return nova


def simular_paralelo_final(n, iteracoes, num_threads=4, prob_arvore=0.6, prob_crescimento=0.01, prob_fogo=0.0001):
    """Versão final da simulação paralela."""
    matriz = criar_matriz(n, prob_arvore)

    inicio = time.time()
    for _ in range(iteracoes):
        if n >= 400:  # Só usa paralelo para matrizes grandes
            matriz = proximo_estado_paralelo_otimizado(matriz, num_threads, prob_crescimento, prob_fogo)
        else:
            # Para matrizes menores, sequencial é mais rápido
            nova = [[VAZIO for _ in range(n)] for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    cel = matriz[i][j]
                    if cel == VAZIO:
                        nova[i][j] = ARVORE if random.random() < prob_crescimento else VAZIO
                    elif cel == ARVORE:
                        if random.random() < prob_fogo or contar_vizinhos_fogo(matriz, i, j) > 0:
                            nova[i][j] = FOGO
                        else:
                            nova[i][j] = ARVORE
                    else:
                        nova[i][j] = VAZIO
            matriz = nova
    fim = time.time()
    
    return fim - inicio


def benchmark_final():
    """Benchmark final com foco na utilidade prática."""
    print("🎯 BENCHMARK FINAL - THREADS EM FOREST FIRE")
    print("=" * 55)
    
    # Importa sequencial
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.sequencial import simular
    
    print("\nObjetivo: Encontrar cenários onde threads ajudam\n")
    
    # Configurações que podem se beneficiar de paralelismo
    cenarios = [
        {"n": 600, "iter": 15, "nome": "Grande (600x600)"},
        {"n": 1000, "iter": 10, "nome": "Muito Grande (1000x1000)"},
        {"n": 1500, "iter": 5, "nome": "Gigante (1500x1500)"},
    ]
    
    for cenario in cenarios:
        n = cenario["n"]
        iteracoes = cenario["iter"]
        nome = cenario["nome"]
        
        print(f"🔥 {nome} - {iteracoes} iterações")
        print("-" * 50)
        
        # Sequencial
        tempo_seq = simular(n, iteracoes)
        print(f"Sequencial:\t{tempo_seq:.3f}s")
        
        # Teste com diferentes threads
        melhor_tempo = tempo_seq
        melhor_threads = 1
        
        print("\nThreads\tTempo\tSpeedup\tMelhoria")
        print("-" * 40)
        
        for threads in [2, 4, 6, 8]:
            tempo_par = simular_paralelo_final(n, iteracoes, threads)
            speedup = tempo_seq / tempo_par
            melhoria = ((tempo_seq - tempo_par) / tempo_seq) * 100
            
            if tempo_par < melhor_tempo:
                melhor_tempo = tempo_par
                melhor_threads = threads
            
            status = "✅" if speedup > 1.05 else "❌" if speedup < 0.95 else "⚖️"
            print(f"{threads}\t{tempo_par:.3f}s\t{speedup:.2f}x\t{melhoria:+.1f}% {status}")
        
        print(f"\n🏆 Melhor: {melhor_threads} threads ({melhor_tempo:.3f}s)")
        economia = ((tempo_seq - melhor_tempo) / tempo_seq) * 100
        print(f"💰 Economia: {economia:.1f}% de tempo\n")


if __name__ == "__main__":
    benchmark_final()