import sys

def busca_rep(lista):
    if not lista:
        return []
    head, *tail = lista
    restante_repetidos = busca_rep(tail)
    if head in tail and head not in restante_repetidos:
        return [head] + restante_repetidos
    return restante_repetidos

def main():
    linha = sys.stdin.readline()
    if linha:
        #ou .split(',') e .strip() para remover espaços, caso a entrada seja "1, 2, 3, 4"
        numeros = list(map(int, linha.split()))
        resultado = busca_rep(numeros)
        if resultado:
            # * é um operador de desempacotamento para a saída sair limpa, sem colchetes etc
            print(*(resultado))

if __name__ == "__main__":
    main()