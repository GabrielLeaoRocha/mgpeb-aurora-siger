"""
mgpeb.py - Script Principal do MGPEB (Módulo de Gerenciamento de Pouso e Estabilização de Base)

Missão Aurora Siger - Atividade Integradora Fase 2 - FIAP

Protótipo que integra:
- Cadastro de módulos em estruturas lineares (fila, pilha, lista)
- Busca linear por ID, menor combustível e maior prioridade
- Ordenação por prioridade (bubble sort) e combustível (selection sort)
- Simulação de autorização de pouso com lógica booleana

Restrição: sem bibliotecas externas, apenas manipulação básica de dados.
"""

import os
import sys

# Adiciona o diretório src ao path para imports locais
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from estruturas import (
    FilaPouso,
    PilhaHistorico,
    buscar_maior_prioridade,
    buscar_menor_combustivel,
    buscar_por_id,
    ordenar_por_combustivel,
    ordenar_por_prioridade,
)
from decisao import autorizar_pouso, formatar_resultado


# =============================================================================
# CARREGAMENTO DE DADOS CSV
# =============================================================================

def carregar_modulos(caminho):
    """Carrega módulos do arquivo CSV (separador ;)."""
    modulos = []
    with open(caminho, "r", encoding="utf-8") as f:
        cabecalho = f.readline().strip().split(";")
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue
            valores = linha.split(";")
            modulo = {}
            for i, campo in enumerate(cabecalho):
                valor = valores[i]
                if campo in ("prioridade", "integridade_sensores",
                             "condicao_atmosferica", "area_disponivel"):
                    modulo[campo] = int(valor)
                elif campo in ("combustivel_pct", "massa_ton", "horario_chegada_h",
                               "altitude_km", "velocidade_ms",
                               "temp_externa_c", "temp_interna_c"):
                    modulo[campo] = float(valor)
                else:
                    modulo[campo] = valor
            modulos.append(modulo)
    return modulos


# =============================================================================
# EXIBIÇÃO
# =============================================================================

def exibir_modulo(modulo):
    """Exibe os dados de um módulo de forma formatada."""
    print(f"  [{modulo['id']}] {modulo['nome']}")
    print(f"    Prioridade: {modulo['prioridade']} | "
          f"Combustivel: {modulo['combustivel_pct']}% | "
          f"Massa: {modulo['massa_ton']}t | "
          f"Criticidade: {modulo['criticidade']}")
    print(f"    Sensores: {'OK' if modulo['integridade_sensores'] == 1 else 'FALHA'} | "
          f"Atmosfera: {'OK' if modulo['condicao_atmosferica'] == 1 else 'ADVERSA'} | "
          f"Area: {'LIVRE' if modulo['area_disponivel'] == 1 else 'OCUPADA'}")


def exibir_lista(lista, titulo):
    """Exibe uma lista de módulos com título."""
    print(f"\n{'=' * 60}")
    print(f"  {titulo} ({len(lista)} modulos)")
    print(f"{'=' * 60}")
    if not lista:
        print("  [vazio]")
        return
    for modulo in lista:
        exibir_modulo(modulo)
        print()


# =============================================================================
# MENU PRINCIPAL
# =============================================================================

def menu_principal():
    """Exibe o menu principal e retorna a opção escolhida."""
    print("\n" + "=" * 60)
    print("  MGPEB - Modulo de Gerenciamento de Pouso")
    print("  Missao Aurora Siger")
    print("=" * 60)
    print("  1 - Visualizar fila de pouso")
    print("  2 - Buscar modulo por ID")
    print("  3 - Buscar modulo com menor combustivel")
    print("  4 - Buscar modulo com maior prioridade")
    print("  5 - Ordenar fila por prioridade (Bubble Sort)")
    print("  6 - Ordenar fila por combustivel (Selection Sort)")
    print("  7 - Simular autorizacao de pouso (proximo da fila)")
    print("  8 - Simular autorizacao de todos os modulos")
    print("  9 - Visualizar modulos pousados")
    print(" 10 - Visualizar modulos em alerta")
    print(" 11 - Visualizar historico de operacoes (pilha)")
    print("  0 - Sair")
    print("-" * 60)
    return input("  Opcao: ").strip()


def executar():
    """Loop principal do sistema MGPEB."""
    # Caminho relativo ao diretório do script
    dir_script = os.path.dirname(os.path.abspath(__file__))
    caminho_csv = os.path.join(dir_script, "..", "dados", "modulos_fila_pouso.csv")

    # Carrega módulos do CSV
    modulos = carregar_modulos(caminho_csv)
    print(f"\n  {len(modulos)} modulos carregados de {os.path.basename(caminho_csv)}")

    # Inicializa estruturas de dados
    fila = FilaPouso()
    pilha = PilhaHistorico()
    lista_pousados = []
    lista_alerta = []

    # Popula fila com módulos (ordem de chegada)
    for m in modulos:
        fila.enqueue(m)
    pilha.push(f"Sistema inicializado com {len(modulos)} modulos na fila")

    while True:
        opcao = menu_principal()

        if opcao == "1":
            exibir_lista(fila.listar(), "FILA DE POUSO (ordem atual)")
            print(f"  Representacao: {fila}")

        elif opcao == "2":
            id_busca = input("  ID do modulo (ex: HAB-01): ").strip().upper()
            resultado = buscar_por_id(fila.listar(), id_busca)
            if resultado:
                print(f"\n  Modulo encontrado:")
                exibir_modulo(resultado)
            else:
                resultado = buscar_por_id(lista_pousados, id_busca)
                if resultado:
                    print(f"\n  Modulo encontrado (ja pousado):")
                    exibir_modulo(resultado)
                else:
                    print(f"\n  Modulo '{id_busca}' nao encontrado.")

        elif opcao == "3":
            todos = fila.listar()
            resultado = buscar_menor_combustivel(todos)
            if resultado:
                print(f"\n  Modulo com MENOR combustivel na fila:")
                exibir_modulo(resultado)
            else:
                print("\n  Fila vazia.")

        elif opcao == "4":
            todos = fila.listar()
            resultado = buscar_maior_prioridade(todos)
            if resultado:
                print(f"\n  Modulo com MAIOR prioridade na fila:")
                exibir_modulo(resultado)
            else:
                print("\n  Fila vazia.")

        elif opcao == "5":
            itens = fila.listar()
            ordenados = ordenar_por_prioridade(itens)
            exibir_lista(ordenados, "FILA ORDENADA POR PRIORIDADE (Bubble Sort)")
            pilha.push("Fila ordenada por prioridade (Bubble Sort)")

        elif opcao == "6":
            itens = fila.listar()
            ordenados = ordenar_por_combustivel(itens)
            exibir_lista(ordenados, "FILA ORDENADA POR COMBUSTIVEL (Selection Sort)")
            pilha.push("Fila ordenada por combustivel (Selection Sort)")

        elif opcao == "7":
            proximo = fila.front()
            if proximo is None:
                print("\n  Fila vazia. Nenhum modulo para processar.")
                continue
            resultado = autorizar_pouso(proximo)
            print("\n" + formatar_resultado(proximo["id"], resultado))

            if resultado["decisao"] == "AUTORIZADO":
                modulo = fila.dequeue()
                lista_pousados.append(modulo)
                pilha.push(f"Pouso AUTORIZADO: {modulo['id']}")
                print(f"  >> {modulo['id']} removido da fila e adicionado aos pousados.")

            elif resultado["decisao"] == "EMERGENCIA":
                modulo = fila.dequeue()
                lista_pousados.append(modulo)
                lista_alerta.append(modulo)
                pilha.push(f"Pouso de EMERGENCIA: {modulo['id']}")
                print(f"  >> {modulo['id']} pousado em emergencia (adicionado a pousados e alertas).")

            elif resultado["decisao"] == "ESPERA":
                pilha.push(f"Modulo em ESPERA: {proximo['id']} - {resultado['motivo']}")
                print(f"  >> {proximo['id']} permanece na fila aguardando condicoes.")

            else:
                modulo = fila.dequeue()
                lista_alerta.append(modulo)
                pilha.push(f"Pouso ABORTADO: {modulo['id']} - {resultado['motivo']}")
                print(f"  >> {modulo['id']} removido da fila e adicionado aos alertas.")

        elif opcao == "8":
            print("\n  Simulando autorizacao para todos os modulos da fila...")
            print("-" * 60)
            itens = fila.listar()
            contadores = {"AUTORIZADO": 0, "EMERGENCIA": 0, "ESPERA": 0, "ABORTADO": 0}
            for modulo in itens:
                resultado = autorizar_pouso(modulo)
                contadores[resultado["decisao"]] += 1
                status = resultado["decisao"]
                c = resultado["condicoes"]
                bits = f"C={1 if c['C'] else 0} A={1 if c['A'] else 0} D={1 if c['D'] else 0} S={1 if c['S'] else 0}"
                print(f"  [{modulo['id']:8}] {status:12} | {bits} | {resultado['motivo']}")
            print("-" * 60)
            print(f"  Resumo: {contadores['AUTORIZADO']} autorizados, "
                  f"{contadores['EMERGENCIA']} emergencias, "
                  f"{contadores['ESPERA']} em espera, "
                  f"{contadores['ABORTADO']} abortados")
            pilha.push("Simulacao completa de todos os modulos executada")

        elif opcao == "9":
            exibir_lista(lista_pousados, "MODULOS POUSADOS")

        elif opcao == "10":
            exibir_lista(lista_alerta, "MODULOS EM ALERTA")

        elif opcao == "11":
            print(f"\n  HISTORICO DE OPERACOES (Pilha - {pilha.size()} registros):")
            print(f"  {pilha}")

        elif opcao == "0":
            print("\n  Sistema MGPEB encerrado. Missao Aurora Siger.")
            pilha.push("Sistema encerrado")
            break

        else:
            print("\n  Opcao invalida. Tente novamente.")


# =============================================================================
# PONTO DE ENTRADA
# =============================================================================

if __name__ == "__main__":
    executar()
