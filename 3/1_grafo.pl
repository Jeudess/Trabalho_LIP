
cidade(cidade1).
cidade(cidade2).
cidade(cidade3).
cidade(cidade4).
cidade(cidade5).
cidade(cidade6).
cidade(cidade7).

% Representação do grafo: arestas bidirecionais
conectado(cidade1, cidade2).
conectado(cidade2, cidade1).

conectado(cidade1, cidade3).
conectado(cidade3, cidade1).

conectado(cidade2, cidade4).
conectado(cidade4, cidade2).

conectado(cidade3, cidade4).
conectado(cidade4, cidade3).

conectado(cidade5, cidade6).
conectado(cidade6, cidade5).


contar_vizinhos(Cidade, N) :-
    findall(Vizinho, conectado(Cidade, Vizinho), Vizinhos), 
    length(Vizinhos, N).


% Auxiliar: Coleta todas as cidades únicas que possuem alguma conexão
obter_todas_cidades(Cidades) :-
    findall(C, cidade(C), Cidades).

maior_vizinhanca(Cidades, CidadeComMaiorVizinhanca) :-
    obter_todas_cidades(Cidades), 
    maior_vizinhanca_aux(Cidades, -1, '', CidadeComMaiorVizinhanca).

maior_vizinhanca_aux([], _, MaiorCidadeAtual, MaiorCidadeAtual).
maior_vizinhanca_aux([H|T], MaxVizinhosAtual, CidadeAtual, CidadeComMaiorVizinhanca) :-
    contar_vizinhos(H, N),
    (N > MaxVizinhosAtual ->
        maior_vizinhanca_aux(T, N, H, CidadeComMaiorVizinhanca)
    ;
        maior_vizinhanca_aux(T, MaxVizinhosAtual, CidadeAtual, CidadeComMaiorVizinhanca)
    ).

verifica_ilha(Cidades, X) :-
    obter_todas_cidades(Cidades), 
    member(X, Cidades),        
    contar_vizinhos(X, 0).