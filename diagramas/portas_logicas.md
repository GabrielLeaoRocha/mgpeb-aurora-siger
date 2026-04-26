# Diagrama de Portas Lógicas - Sistema de Decisão MGPEB

## Variáveis de Entrada

| Variável | Descrição | Condição para 1 |
|----------|-----------|-----------------|
| C | Combustível suficiente | combustível >= 30% |
| A | Atmosfera OK | sem tempestade |
| D | Área disponível | slot livre |
| S | Sensores operacionais | integridade = 1 |

## Expressões Booleanas e Portas Lógicas

```mermaid
flowchart LR
    subgraph ENTRADAS
        C[C - Combustível]
        A[A - Atmosfera]
        D[D - Área]
        S[S - Sensores]
    end

    subgraph POUSO_AUTORIZADO ["POUSO_AUTORIZADO = C AND A AND D AND S"]
        AND1((AND))
    end
    C --> AND1
    A --> AND1
    D --> AND1
    S --> AND1
    AND1 --> PA[POUSO_AUTORIZADO]

    subgraph ALERTA_EXPR ["ALERTA = (NOT C) OR (NOT S)"]
        NOT_C1((NOT)) 
        NOT_S1((NOT))
        OR1((OR))
    end
    C --> NOT_C1
    S --> NOT_S1
    NOT_C1 --> OR1
    NOT_S1 --> OR1
    OR1 --> AL[ALERTA]

    subgraph EMERGENCIA_EXPR ["EMERGENCIA = (NOT C) AND S AND D"]
        NOT_C2((NOT))
        AND2((AND))
    end
    C --> NOT_C2
    NOT_C2 --> AND2
    S --> AND2
    D --> AND2
    AND2 --> EM[EMERGENCIA]

    subgraph ESPERA_EXPR ["ESPERA = (NOT A) OR (NOT D)"]
        NOT_A1((NOT))
        NOT_D1((NOT))
        OR2((OR))
    end
    A --> NOT_A1
    D --> NOT_D1
    NOT_A1 --> OR2
    NOT_D1 --> OR2
    OR2 --> ES[ESPERA]

    style PA fill:#2d6a4f,color:#fff
    style AL fill:#e9c46a,color:#000
    style EM fill:#e63946,color:#fff
    style ES fill:#f4a261,color:#000
```

## Tabela-Verdade Resumida (casos chave)

| C | A | D | S | AUTORIZADO | ALERTA | EMERGÊNCIA | ESPERA |
|---|---|---|---|:---:|:---:|:---:|:---:|
| 1 | 1 | 1 | 1 | **1** | 0 | 0 | 0 |
| 0 | 1 | 1 | 1 | 0 | **1** | **1** | 0 |
| 1 | 0 | 1 | 1 | 0 | 0 | 0 | **1** |
| 1 | 1 | 0 | 1 | 0 | 0 | 0 | **1** |
| 1 | 1 | 1 | 0 | 0 | **1** | 0 | 0 |
| 0 | 1 | 0 | 1 | 0 | **1** | 0 | **1** |
| 0 | 0 | 1 | 0 | 0 | **1** | 0 | **1** |
