
adiciona_inicio(X, L1, [X|L1]).


remove_elemento(X, [X|T], T).
remove_elemento(X, [H|T], [H|TT]) :- remove_elemento(X, T, TT). 


junta_listas([], L, L).
junta_listas([H|L1], L2, [H|L3]) :- junta_listas(L1, L2, L3).


pertence(X, [X|_]).
pertence(X, [_|T]) :- pertence(X, T).


tamanho(0, []).
tamanho(N, [_|T]) :- 
	tamanho(M, T),
	N is M + 1.
