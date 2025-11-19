🌲🔥 Modelo Forest Fire — Versão Sequencial

Implementação sequencial do modelo Forest Fire para a disciplina de Sistemas Distribuídos.

📌 Objetivo

Implementar a versão sequencial do modelo Forest Fire, que será usada como referência para:

Implementação paralela (threads)

Implementação distribuída (sockets ou RMI)

Comparação de desempenho entre as três abordagens

🔥 Como funciona o modelo

O ambiente é uma matriz N × N, onde cada célula pode estar em um dos estados:

0 — Vazio
1 — Árvore
2 — Pegando fogo


A cada iteração da simulação:

Células vazias continuam vazias.

Árvores:

Pegam fogo se um vizinho está queimando

Podem pegar fogo espontaneamente com probabilidade f

Células em fogo viram vazio no próximo passo

Este é um autômato celular clássico, muito usado para simular propagação rápida.
