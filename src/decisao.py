"""
decisao.py - Lógica de Autorização de Pouso do MGPEB

Implementa as regras de decisão usando lógica booleana (portas lógicas):
- POUSO_AUTORIZADO = C AND A AND D AND S
- ALERTA           = (NOT C) OR (NOT S)
- EMERGENCIA       = (NOT C) AND S AND D
- ESPERA           = (NOT A) OR (NOT D)

Variáveis booleanas:
  C = combustível suficiente (>= 30%)
  A = condição atmosférica OK (sem tempestade)
  D = área de pouso disponível
  S = sensores operacionais (integridade OK)

Restrição: sem bibliotecas externas, decisões via if/elif/else.
"""

# Limiar mínimo de combustível para pouso normal (%)
COMBUSTIVEL_MINIMO = 30.0


def avaliar_condicoes(modulo):
    """Avalia as 4 condições booleanas de um módulo.

    Retorna dicionário com os valores de C, A, D e S.
    """
    c = modulo["combustivel_pct"] >= COMBUSTIVEL_MINIMO
    a = modulo["condicao_atmosferica"] == 1
    d = modulo["area_disponivel"] == 1
    s = modulo["integridade_sensores"] == 1
    return {"C": c, "A": a, "D": d, "S": s}


def autorizar_pouso(modulo):
    """Aplica as regras de decisão booleana para um módulo.

    Retorna dicionário com:
      - decisao: "AUTORIZADO", "EMERGENCIA", "ESPERA" ou "ABORTADO"
      - condicoes: valores de C, A, D, S
      - pouso_autorizado: bool (C AND A AND D AND S)
      - alerta: bool ((NOT C) OR (NOT S))
      - emergencia: bool ((NOT C) AND S AND D)
      - espera: bool ((NOT A) OR (NOT D))
      - motivo: descrição textual da decisão
    """
    cond = avaliar_condicoes(modulo)
    c, a, d, s = cond["C"], cond["A"], cond["D"], cond["S"]

    # Expressões booleanas (portas lógicas)
    pouso_autorizado = c and a and d and s
    alerta = (not c) or (not s)
    emergencia = (not c) and s and d
    espera = (not a) or (not d)

    # Decisão por prioridade (if/elif/else encadeado)
    if pouso_autorizado:
        decisao = "AUTORIZADO"
        motivo = "Todos os parametros dentro da faixa segura"
    elif emergencia:
        decisao = "EMERGENCIA"
        motivo = "Combustivel critico - pouso de emergencia autorizado"
    elif espera:
        motivos_espera = []
        if not a:
            motivos_espera.append("condicao atmosferica adversa")
        if not d:
            motivos_espera.append("area de pouso indisponivel")
        motivo = "Modulo em espera: " + " e ".join(motivos_espera)
        decisao = "ESPERA"
    else:
        decisao = "ABORTADO"
        motivos_abort = []
        if not c:
            motivos_abort.append("combustivel insuficiente")
        if not s:
            motivos_abort.append("falha nos sensores")
        if not a:
            motivos_abort.append("condicao atmosferica adversa")
        if not d:
            motivos_abort.append("area indisponivel")
        motivo = "Procedimento abortado: " + ", ".join(motivos_abort)
        decisao = "ABORTADO"

    return {
        "decisao": decisao,
        "condicoes": cond,
        "pouso_autorizado": pouso_autorizado,
        "alerta": alerta,
        "emergencia": emergencia,
        "espera": espera,
        "motivo": motivo,
    }


def formatar_resultado(modulo_id, resultado):
    """Formata o resultado da decisão para exibição."""
    cond = resultado["condicoes"]
    linhas = [
        f"{'=' * 60}",
        f"  MODULO: {modulo_id}",
        f"  DECISAO: {resultado['decisao']}",
        f"{'=' * 60}",
        f"  Condicoes booleanas:",
        f"    C (combustivel >= {COMBUSTIVEL_MINIMO}%): {'1' if cond['C'] else '0'}",
        f"    A (atmosfera OK):          {'1' if cond['A'] else '0'}",
        f"    D (area disponivel):       {'1' if cond['D'] else '0'}",
        f"    S (sensores OK):           {'1' if cond['S'] else '0'}",
        f"  Saidas logicas:",
        f"    POUSO_AUTORIZADO (C AND A AND D AND S): {1 if resultado['pouso_autorizado'] else 0}",
        f"    ALERTA (NOT C OR NOT S):               {1 if resultado['alerta'] else 0}",
        f"    EMERGENCIA (NOT C AND S AND D):         {1 if resultado['emergencia'] else 0}",
        f"    ESPERA (NOT A OR NOT D):                {1 if resultado['espera'] else 0}",
        f"  Motivo: {resultado['motivo']}",
        f"{'=' * 60}",
    ]
    return "\n".join(linhas)
