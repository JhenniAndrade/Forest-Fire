import random
import time

# Estados possíveis
VAZIO = 0
ARVORE = 1
FOGO = 2


def criar_matriz(n, prob_arvore=0.6):
    """Cria uma matriz nxn com árvores distribuídas aleatoriamente. Cada célula tem prob_arvore de ser uma árvore"""
    return [
        [ARVORE if random.random() < prob_arvore else VAZIO for _ in range(n)]
        for _ in range(n)
    ]


def vizinhos(i, j, n):
    """Retorna a lista de coordenadas dos vizinhos (8 vizinhos). Consideramos a vizinhança de Moore"""
    coords = []
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < n:
                coords.append((ni, nj))
    return coords


def proximo_estado(matriz, prob_crescimento=0.01, prob_fogo=0.0001):
    """Calcula o próximo estado da matriz conforme o modelo Forest Fire
    Regras:
    - Espaço vazio pode virar árvore com prob_crescimento
    - Árvore pode pegar fogo:
        - espontaneamente (prob_fogo)
        - ou se qualquer vizinho está em chamas
    - Fogo vira VAZIO"""
    n = len(matriz)
    nova = [[VAZIO for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            cel = matriz[i][j]

            # Se está vazio → pode nascer árvore
            if cel == VAZIO:
                nova[i][j] = ARVORE if random.random() < prob_crescimento else VAZIO

            # Se é árvore → pode pegar fogo
            elif cel == ARVORE:
                if random.random() < prob_fogo:
                    nova[i][j] = FOGO
                else:
                    queimando = any(
                        matriz[x][y] == FOGO for x, y in vizinhos(i, j, n)
                    )
                    nova[i][j] = FOGO if queimando else ARVORE

            # Se está pegando fogo → vira vazio
            elif cel == FOGO:
                nova[i][j] = VAZIO

    return nova


def simular(n, iteracoes, prob_arvore=0.6, prob_crescimento=0.01, prob_fogo=0.0001):
    """Executa a simulação sequencial completa e retorna o tempo gasto"""
    matriz = criar_matriz(n, prob_arvore)

    inicio = time.time()

    for _ in range(iteracoes):
        matriz = proximo_estado(matriz, prob_crescimento, prob_fogo)

    fim = time.time()
    return fim - inicio


if __name__ == "__main__":
    # Execução simples para teste
    n = 200
    iteracoes = 200

    tempo = simular(n, iteracoes)
    print(f"Tempo sequencial: {tempo:.4f} segundos")
