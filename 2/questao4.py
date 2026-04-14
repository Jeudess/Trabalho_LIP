import sys

def calcular_estatisticas(lista, soma_a=0.0, soma_h=0.0, contagem=0):
    if not lista:
        return (soma_a / contagem, contagem / soma_h)
    head, *tail = lista
    return calcular_estatisticas(tail, soma_a + head, soma_h + (1/head), contagem + 1)

def main():
    linha = sys.stdin.readline()
    if linha:
        numeros = list(map(float, linha.split()))
        print(calcular_estatisticas(numeros))

if __name__ == "__main__":
    main()