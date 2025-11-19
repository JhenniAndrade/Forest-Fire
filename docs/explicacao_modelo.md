# Modelo Forest Fire – Explicação do Funcionamento

O modelo Forest Fire é um autômato celular usado para simular a propagação de fogo em uma floresta. Ele utiliza uma grade/matriz onde cada célula representa uma parte da floresta.

## Estados possíveis
Cada célula pode estar em um dos três estados:

- **0 – Vazio**  
- **1 – Árvore**  
- **2 – Pegando fogo**

## Regras de evolução
A cada iteração, o estado da matriz muda seguindo três regras principais:

### 1. Crescimento de árvores
Um espaço vazio (**0**) pode se tornar árvore (**1**) com uma probabilidade *p* (prob_crescimento).

### 2. Fogo começa
Uma árvore (**1**) pode pegar fogo de duas formas:

- **Espontaneamente**, com probabilidade *f* (prob_fogo);
- **Pela vizinhança**, caso qualquer um dos 8 vizinhos esteja pegando fogo.

### 3. Fogo se apaga
Uma célula pegando fogo (**2**) vira vazia (**0**) na próxima iteração.

## Vizinhança
Usamos **vizinhança de Moore**, onde cada célula tem até 8 vizinhos ao redor.

## Parâmetros utilizados
- Tamanho da matriz (N × N)
- Número de iterações
- Probabilidade de crescimento de árvores (p)
- Probabilidade de uma árvore pegar fogo espontaneamente (f)

## Objetivo
Implementamos este modelo em três versões:
1. Sequencial (base)
2. Paralela (threads)
3. Distribuída (sockets/RMI)

A versão sequencial é a referência para medir desempenho e correto funcionamento.
