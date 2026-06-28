
progenitor(roberto, lucas).
progenitor(roberto, marina).
progenitor(carla, lucas).
progenitor(carla, marina).

progenitor(lucas, pedro).

progenitor(marina, sofia).

progenitor(pedro, daniel).
progenitor(sofia, daniel).

sexo(roberto, masculino).
sexo(lucas, masculino).
sexo(pedro, masculino).
sexo(daniel, masculino).
sexo(carla, feminino).
sexo(marina, feminino).
sexo(sofia, feminino).

irma(X, Y) :-
	X \== Y,
	sexo(X, feminino), 
	progenitor(Z, X),
	progenitor(Z, Y).

irmao(X, Y) :-
	X \== Y, 
	sexo(X, masculino),
	progenitor(Z, X),
	progenitor(Z, Y).


mae(X, Y) :- 
	sexo(X, feminino),
	progenitor(X, Y).

pai(X, Y) :-
	sexo(X, masculino),
	progenitor(X, Y).

#AVÔ
avou(X, Y) :-
	progenitor(X, Z),
	progenitor(Z, Y),
	sexo(X, masculino).
#AVÓ
avo(X, Y) :-
	progenitor(X, Z),
	progenitor(Z, Y),
	sexo(X, feminino).


tia(X, Y) :-
	irma(X, Z),
	progenitor(Z, Y).

tio(X, Y) :-
	irmao(X, Z),
	progenitor(Z, Y).

primo(X, Y) :- 
	X \== Y,
	sexo(X, masculino),
	(irmao(Z, A);
	irma(Z, A)), 
	progenitor(Z, X), 
	progenitor(A, Y). 
	
prima(X, Y) :-	
	X \== Y,
	sexo(X, feminino),
	(irmao(Z, A);
	irma(Z, A)),
	progenitor(Z, X),
	progenitor(A, Y).

descendente(X, Y) :- progenitor(Y, X).
descendente(X, Z) :- 
	progenitor(Y, X),
	descendente(Y, Z).