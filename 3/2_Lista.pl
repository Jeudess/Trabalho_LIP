# Questões 2. Implemente os seguintes predicados genéricos sobre listas (sem utilizar o módulo lists 
# do SWI-Prolog):
#  adiciona_inicio(X, L1, L2) → L2 é a lista L1 com o elemento X no início
#  remove_elemento(X, L1, L2) → L2 recebe a L1 com a remoção da primeira ocorrência de X
#  junta_listas(L1, L2, L3) → L3 recebe a concatenação das duas listas L1 e L2
#  pertence(X, L) → verifica se um elemento X pertence à lista L
#  tamanho(N, L) → N é o número de elementos da lista L

# adiciona_inicio(X, L1, L2)
adiciona_inicio(X, L1, [X|L1]).

# remove_elemento(X, L1, L2)
remove_elemento(X, [X|T], T).
remove_elemento(X, [H|T], [H|TT]) :- remove_elemento(X, T, TT). 

# junta_listas(L1, L2, L3)
junta_listas([], L, L).
junta_listas([H|L1], L2, [H|L3]) :- junta_listas(L1, L2, L3).

# pertence(X, L)
pertence(X, [X|_]).
pertence(X, [_|T]) :- pertence(X, T).

# tamanho(N, L)
tamanho(0, []).
tamanho(N, [_|T]) :- 
	tamanho(M, T),
	N is M + 1.
