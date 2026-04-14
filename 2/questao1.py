import sys

def soma_pares(lista):
    if not lista:
        return 0
    head, *tail = lista
    return (head if head % 2 == 0 else 0) + soma_pares(tail)

def main():
     linha = sys.stdin.readline()
     if linha:
        numeros = list(map(int, linha.split()))
        print(soma_pares(numeros))

if __name__ == "__main__":
    main()