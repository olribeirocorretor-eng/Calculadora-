#!/usr/bin/env python3
"""SINDMUNICIPAIS Registro - calculadora de linha de comando."""

import os
import re
import sys

# Paleta da interface: branco, vermelho e verde.
_USA_CORES = sys.stdout.isatty() and "NO_COLOR" not in os.environ

RESET = "\033[0m" if _USA_CORES else ""
NEGRITO = "\033[1m" if _USA_CORES else ""
BRANCO = "\033[97m" if _USA_CORES else ""
VERMELHO = "\033[91m" if _USA_CORES else ""
VERDE = "\033[92m" if _USA_CORES else ""
FUNDO_VERMELHO = "\033[41m" if _USA_CORES else ""
FUNDO_BRANCO = "\033[107m" if _USA_CORES else ""
FUNDO_VERDE = "\033[42m" if _USA_CORES else ""

# Pessoa estilizada do logotipo: figura branca (W) com a "sombra" verde (G)
# sobre fundo vermelho (.). Cada célula ocupa dois caracteres no terminal.
SIMBOLO = [
    "......WWWGG.....",
    ".....WWWWWGG....",
    "......WWWGG.....",
    "WWWWWWWWGGGGGGGG",
    "...WWWWWGGGG....",
    "....WWWW.GGG....",
    "...WWW...GGG....",
    "..WWW.....GG....",
    ".WW........G....",
]

TITULO = [
    "",
    "",
    "",
    f"{NEGRITO}{BRANCO}SINDMUNICIPAIS",
    f"{VERDE}{NEGRITO}Registro",
    "",
    f"{BRANCO}Calculadora",
    "",
    "",
]


def somar(a, b):
    return a + b


def subtrair(a, b):
    return a - b


def multiplicar(a, b):
    return a * b


def dividir(a, b):
    if b == 0:
        raise ZeroDivisionError("Não é possível dividir por zero.")
    return a / b


OPERACOES = {
    "1": ("Somar", "+", somar),
    "2": ("Subtrair", "-", subtrair),
    "3": ("Multiplicar", "*", multiplicar),
    "4": ("Dividir", "/", dividir),
}


def ler_numero(mensagem):
    while True:
        valor = input(mensagem).strip().replace(",", ".")
        try:
            return float(valor)
        except ValueError:
            print(f"{VERMELHO}Valor inválido. Digite um número.{RESET}")


def formatar(numero):
    return int(numero) if numero == int(numero) else numero


def _celula(caractere):
    if not _USA_CORES:
        return {"W": "██", "G": "▓▓"}.get(caractere, "  ")
    fundo = {"W": FUNDO_BRANCO, "G": FUNDO_VERDE}.get(caractere, FUNDO_VERMELHO)
    return f"{fundo}  "


def _sem_cores(texto):
    return re.sub(r"\033\[[0-9;]*m", "", texto)


def exibir_cabecalho():
    largura_texto = 26
    for linha, texto in zip(SIMBOLO, TITULO):
        figura = "".join(_celula(c) for c in linha)
        preenchimento = " " * (largura_texto - len(_sem_cores(texto)))
        print(f"{figura}{FUNDO_VERMELHO}  {texto}{FUNDO_VERMELHO}{preenchimento}{RESET}")
    print(f"{VERDE}{'━' * (len(SIMBOLO[0]) * 2 + 2 + largura_texto)}{RESET}")


def main():
    exibir_cabecalho()
    while True:
        print()
        for chave, (nome, simbolo, _) in OPERACOES.items():
            print(f"{VERDE}{NEGRITO}{chave}.{RESET} {nome} ({simbolo})")
        print(f"{VERMELHO}{NEGRITO}0.{RESET} Sair")

        opcao = input("Escolha uma opção: ").strip()
        if opcao == "0":
            print("Até logo!")
            break
        if opcao not in OPERACOES:
            print(f"{VERMELHO}Opção inválida. Tente novamente.{RESET}")
            continue

        _, simbolo, funcao = OPERACOES[opcao]
        a = ler_numero("Primeiro número: ")
        b = ler_numero("Segundo número: ")

        try:
            resultado = funcao(a, b)
        except ZeroDivisionError as erro:
            print(f"{VERMELHO}Erro: {erro}{RESET}")
            continue

        print(f"{VERDE}{NEGRITO}Resultado:{RESET} {formatar(a)} {simbolo} {formatar(b)} = {formatar(resultado)}")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nAté logo!")
