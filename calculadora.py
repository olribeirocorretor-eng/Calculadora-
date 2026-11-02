#!/usr/bin/env python3
"""Calculadora simples de linha de comando."""


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
            print("Valor inválido. Digite um número.")


def formatar(numero):
    return int(numero) if numero == int(numero) else numero


def main():
    print("=== Calculadora Simples ===")
    while True:
        print()
        for chave, (nome, simbolo, _) in OPERACOES.items():
            print(f"{chave}. {nome} ({simbolo})")
        print("0. Sair")

        opcao = input("Escolha uma opção: ").strip()
        if opcao == "0":
            print("Até logo!")
            break
        if opcao not in OPERACOES:
            print("Opção inválida. Tente novamente.")
            continue

        _, simbolo, funcao = OPERACOES[opcao]
        a = ler_numero("Primeiro número: ")
        b = ler_numero("Segundo número: ")

        try:
            resultado = funcao(a, b)
        except ZeroDivisionError as erro:
            print(f"Erro: {erro}")
            continue

        print(f"Resultado: {formatar(a)} {simbolo} {formatar(b)} = {formatar(resultado)}")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nAté logo!")
