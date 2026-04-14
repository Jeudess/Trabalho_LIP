import sys

def soma_sucessiva(n):
    if n <= 0:
        return 0
    return n + soma_sucessiva(n - 1)

def main():
    linha = sys.stdin.readline()
    if linha:
        print(soma_sucessiva(int(linha.strip())))

if __name__ == "__main__":
    main()