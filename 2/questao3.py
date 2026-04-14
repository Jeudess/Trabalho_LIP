import sys

def impares_duplicados(lista):
    if not lista:
        return []
    head, *tail = lista
    resultado_cauda = impares_duplicados(tail)
    if head % 2 != 0 and head in tail and head not in resultado_cauda:
        return [head] + resultado_cauda
    return resultado_cauda

def main():
    linha = sys.stdin.readline()
    if linha:
        numeros = list(map(int, linha.split()))
        resultado = impares_duplicados(numeros)
        if resultado:
            print(*(resultado))

if __name__ == "__main__":
    main()