"""
estruturas.py - Estruturas de Dados Lineares do MGPEB

Implementa as estruturas fundamentais para o gerenciamento de pouso:
- FilaPouso (Queue - FIFO): fila de módulos aguardando autorização
- PilhaHistorico (Stack - LIFO): histórico de operações do sistema
- Funções de busca linear e ordenação (bubble sort, selection sort)

Restrição: sem bibliotecas externas, apenas manipulação básica de dados.
"""


# =============================================================================
# FILA DE POUSO (Queue - FIFO)
# =============================================================================

class FilaPouso:
    """Fila FIFO para módulos aguardando autorização de pouso.

    Primeiro módulo a entrar na fila é o primeiro a ser processado.
    Operações: enqueue, dequeue, front, is_empty, size, listar.
    """

    def __init__(self):
        """Inicializa fila vazia."""
        self._fila = []

    def enqueue(self, modulo):
        """Adiciona módulo ao final da fila."""
        self._fila.append(modulo)

    def dequeue(self):
        """Remove e retorna o módulo do início da fila."""
        if self.is_empty():
            return None
        return self._fila.pop(0)

    def front(self):
        """Retorna o próximo módulo sem removê-lo."""
        if self.is_empty():
            return None
        return self._fila[0]

    def is_empty(self):
        """Verifica se a fila está vazia."""
        return len(self._fila) == 0

    def size(self):
        """Retorna a quantidade de módulos na fila."""
        return len(self._fila)

    def listar(self):
        """Retorna cópia da fila como lista."""
        return list(self._fila)

    def __repr__(self):
        """Representação textual da fila."""
        ids = [m["id"] for m in self._fila]
        return " -> ".join(ids) if ids else "[fila vazia]"


# =============================================================================
# PILHA DE HISTÓRICO (Stack - LIFO)
# =============================================================================

class PilhaHistorico:
    """Pilha LIFO para registro de operações do sistema.

    Última operação registrada é a primeira consultada.
    Operações: push, pop, peek, is_empty, size, listar.
    """

    def __init__(self):
        """Inicializa pilha vazia."""
        self._pilha = []

    def push(self, operacao):
        """Registra nova operação no topo da pilha."""
        self._pilha.append(operacao)

    def pop(self):
        """Remove e retorna a operação do topo."""
        if self.is_empty():
            return None
        return self._pilha.pop()

    def peek(self):
        """Retorna a operação do topo sem removê-la."""
        if self.is_empty():
            return None
        return self._pilha[-1]

    def is_empty(self):
        """Verifica se a pilha está vazia."""
        return len(self._pilha) == 0

    def size(self):
        """Retorna a quantidade de operações na pilha."""
        return len(self._pilha)

    def listar(self):
        """Retorna cópia da pilha como lista (topo primeiro)."""
        return list(reversed(self._pilha))

    def __repr__(self):
        """Representação textual da pilha (topo primeiro)."""
        if self.is_empty():
            return "[pilha vazia]"
        linhas = []
        for i, op in enumerate(reversed(self._pilha)):
            prefixo = "TOP -> " if i == 0 else "       "
            linhas.append(f"{prefixo}[{op}]")
        return "\n".join(linhas)


# =============================================================================
# BUSCA LINEAR
# =============================================================================

def buscar_por_id(lista, id_busca):
    """Busca linear: localiza módulo pelo ID. Complexidade O(n)."""
    for modulo in lista:
        if modulo["id"] == id_busca:
            return modulo
    return None


def buscar_menor_combustivel(lista):
    """Busca linear: retorna módulo com menor nível de combustível. O(n)."""
    if not lista:
        return None
    menor = lista[0]
    for modulo in lista[1:]:
        if modulo["combustivel_pct"] < menor["combustivel_pct"]:
            menor = modulo
    return menor


def buscar_maior_prioridade(lista):
    """Busca linear: retorna módulo com maior prioridade (menor valor). O(n)."""
    if not lista:
        return None
    melhor = lista[0]
    for modulo in lista[1:]:
        if modulo["prioridade"] < melhor["prioridade"]:
            melhor = modulo
    return melhor


# =============================================================================
# ORDENAÇÃO
# =============================================================================

def ordenar_por_prioridade(lista):
    """Bubble Sort: ordena por prioridade de pouso (menor valor = maior prioridade).

    Complexidade: O(n²) no pior caso.
    Justificativa: algoritmo simples, previsível, adequado para hardware limitado.
    """
    copia = list(lista)
    n = len(copia)
    for i in range(n):
        trocou = False
        for j in range(0, n - i - 1):
            if copia[j]["prioridade"] > copia[j + 1]["prioridade"]:
                copia[j], copia[j + 1] = copia[j + 1], copia[j]
                trocou = True
        if not trocou:
            break
    return copia


def ordenar_por_combustivel(lista):
    """Selection Sort: ordena por nível de combustível (menor primeiro = mais urgente).

    Complexidade: O(n²) no pior caso.
    Justificativa: número fixo de trocas, previsível em uso de memória.
    """
    copia = list(lista)
    n = len(copia)
    for i in range(n):
        idx_min = i
        for j in range(i + 1, n):
            if copia[j]["combustivel_pct"] < copia[idx_min]["combustivel_pct"]:
                idx_min = j
        if idx_min != i:
            copia[i], copia[idx_min] = copia[idx_min], copia[i]
    return copia
