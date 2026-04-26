# MGPEB - Módulo de Gerenciamento de Pouso e Estabilização de Base

**Missão Aurora Siger — Atividade Integradora Fase 2 — FIAP**

Protótipo em Python do Módulo de Gerenciamento de Pouso e Estabilização de Base (MGPEB) da missão Aurora Siger. Implementa fila de pouso, listas e pilha de histórico, regras de decisão com lógica booleana (autorizado/espera/alerta/emergência), buscas lineares e ordenações simples (bubble/selection), além de simulações de telemetria para testes. Foco em soluções simples, determinísticas e auditáveis, alinhadas às limitações de hardware embarcado e a princípios ESG.

## Estrutura do Projeto

```
mgpeb-aurora-siger/
├── dados/
│   ├── modulos_fila_pouso.csv          # Módulos aguardando pouso (20 registros)
│   ├── log_operacoes.csv               # Histórico de operações de pouso (42 registros)
│   └── telemetria_descida.csv          # Telemetria detalhada da descida do HAB-01 (40 medições)
├── src/
│   ├── mgpeb.py                        # Script principal
│   ├── estruturas.py                   # Estruturas de dados (fila, pilha, lista)
│   └── decisao.py                      # Lógica de autorização de pouso
├── diagramas/
│   ├── portas_logicas.png              # Diagrama de portas lógicas
│   └── fluxograma_sistema.png          # Fluxograma do sistema de decisão
├── .gitignore
└── README.md
```

## Conceitos Aplicados

- **Portas lógicas e funções booleanas**: Regras de autorização de pouso (AND, OR, NOT)
- **Estruturas de dados lineares**: Fila (FIFO) para ordem de pouso, pilha (LIFO) para histórico, listas para módulos pousados e alertas
- **Algoritmos de busca e ordenação**: Busca linear, bubble sort, selection sort
- **Modelagem matemática**: Consumo de combustível (função quadrática), velocidade de descida (função exponencial)
- **Evolução computacional**: Justificativa das escolhas técnicas com base em limitações de hardware espacial
- **Princípios ESG**: Governança transparente, proteção planetária, gestão sustentável de recursos

## Dados Simulados

Os arquivos CSV na pasta `dados/` simulam cenários variados de operação:

- **Cenários nominais**: Módulos com todos os parâmetros dentro das faixas seguras
- **Cenários de alerta**: Módulos com combustível baixo ou sensores falhando
- **Cenários de emergência**: Pouso forçado por combustível crítico (ex: ENE-02)
- **Cenários de espera**: Condições atmosféricas adversas ou área indisponível

## Requisitos

- Python 3.x (sem bibliotecas externas)

## Como Executar

```bash
python src/mgpeb.py
```

## Autor

- **Gabriel de Leão da Rocha** — rm571330
- Ciência da Computação — 1CCOC — FIAP
