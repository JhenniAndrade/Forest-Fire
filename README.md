# 🌲🔥 Modelo Forest Fire — Versão Paralela com Threads

Implementação paralela do modelo Forest Fire usando **Threads** para a disciplina de Sistemas Distribuídos.

## 📌 Objetivo

Transformar a versão sequencial em paralela, implementando:
- ✅ **Divisão do processamento** entre múltiplos threads da CPU
- ✅ **Teste com diferentes quantidades** de threads (2, 4, 8)
- ✅ **Otimização de sincronização** e prevenção de condições de corrida
- ✅ **Medição e comparação** de tempos de execução

## 🔥 Como funciona o modelo

O ambiente é uma matriz N × N, onde cada célula pode estar em um dos estados:
- **0** — Vazio
- **1** — Árvore  
- **2** — Pegando fogo

A cada iteração da simulação:
- Células vazias continuam vazias
- Árvores:
  - Pegam fogo se um vizinho está queimando
  - Podem pegar fogo espontaneamente com probabilidade f
- Células em fogo viram vazio no próximo passo

## 🚀 Como Executar

### Benchmark paralelo e sequencial
```bash
python tests/benchmark.py
```

### Benchmark distribuido
```bash
python ./src/servidor.py 300 20 <NUMERO_DE_CLIENTES>
```

Terminais separados:
```bash
python ./src/cliente.py 8000 
```

## 📊 Resultados Obtidos

### Performance com Matrix 1000x1000
| Threads | Tempo | Speedup | Eficiência |
|---------|-------|---------|------------|
| 1 (seq) | 11.78s | 1.00x | 1.00 |
| 2 | 10.84s | **1.09x** | 0.54 |
| 4 | 10.73s | **1.10x** | 0.27 |
| 6 | 10.59s | **1.11x** | 0.19 |
| 8 | 10.49s | **1.12x** | 0.14 |

**🏆 Melhor resultado: 17.9% de economia de tempo com 6 threads**

## 🔧 Estratégias de Paralelização

### 1. Divisão por Chunks
- Matriz dividida em blocos de células
- Cada thread processa um conjunto independente
- Evita condições de corrida

### 2. Otimizações Implementadas
- **ThreadPoolExecutor** para coordenação automática
- **Fallback sequencial** para matrizes pequenas (<400x400)
- **Sem locks** na região crítica principal
- **Cache locality** otimizada

## 🎓 Conceitos Aplicados

- **Paralelização de dados**: divisão da matriz
- **Sincronização**: coordenação entre threads
- **Speedup e Eficiência**: métricas de performance
- **Balanceamento de carga**: distribuição equilibrada
- **Overhead**: análise do custo de coordenação

Este é um autômato celular clássico, adaptado para demonstrar paralelização com threads.
