#  Implemente um programa em Prolog sobre a seguinte família fictícia:
#  A família Oliveira possui os seguintes registros:
#  Roberto e Carla são pais de Lucas e Marina
#  Lucas é pai de Pedro
#  Marina é mãe de Sofia
#  Pedro e Sofia tiveram um filho chamado Daniel
#
# a) Utilizando o predicado progenitor(X , Y) represente todas as relações de progenitor da família.

# b) Implemente predicados para representar as seguintes relações:
#  masculino(X) → verdadeiro se X for masculino, falso caso contrário
#  feminino(X) → verdadeiro se X for feminino, falso caso contrário
#  irmao(X,Y) → X é irmão de Y
#  irma(X,Y) → X é irmã de Y
#  pai(X,Y) → X é pai de Y
#  mae(X,Y) → X é mãe de Y
#  avou(X,Y) → X é avô de Y
#  avo(X,Y) → X é avó de Y
#  tio(X,Y) → X é tio de Y
#  tia(X,Y) → X é tia de Y
#  primo(X,Y) → X é primo de Y
#  prima(X,Y) → X é prima de Y
#  descendente(X,Y) → X descende de Y

# Roberto e Carla são pais de Lucas e Marina
progenitor(roberto, lucas).
progenitor(roberto, marina).
progenitor(carla, lucas).
progenitor(carla, marina).

# Lucas é pai de Pedro
progenitor(lucas, pedro).

# Marina é mãe de Sofia
progenitor(marina, sofia).

# Pedro e Sofia tiveram um filho chamado Daniel
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
avo_m(X, Y) :-
	progenitor(X, Z),
	progenitor(Z, Y),
	sexo(X, masculino).
#AVÓ
avo_f(X, Y) :-
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