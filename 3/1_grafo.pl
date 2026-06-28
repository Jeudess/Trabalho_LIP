
# verificar se duas cidades são diretamente conectadas

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

# contar a vizinhança de uma cidade
contar_vizinhos(Cidade, N) :-
    findall(Vizinho, conectado(Cidade, Vizinho), Vizinhos), 
    length(Vizinhos, N).

# encontrar a cidade com a maior vizinhança
maior_vizinhanca(Cidades, CidadeComMaiorVizinhança) :-
    findall(Cidade, (conectado(Cidade, _); conectado(_, Cidade)), TodasCidades),
    list_to_set(TodasCidades, CidadesUnicas), % Remove duplicatas
    maior_vizinhanca_aux(CidadesUnicas, 0, '', CidadeComMaiorVizinhança).

maior_vizinhanca_aux([], _, MaiorCidadeAtual, MaiorCidadeAtual).
maior_vizinhanca_aux([H|T], MaxVizinhosAtual, CidadeAtual, CidadeComMaiorVizinhança) :-
    contar_vizinhos(H, N),
    (N > MaxVizinhosAtual ->
        maior_vizinhanca_aux(T, N, H, CidadeComMaiorVizinhança)
    ;
        maior_vizinhanca_aux(T, MaxVizinhosAtual, CidadeAtual, CidadeComMaiorVizinhança)
    ).

# verificar se uma cidade é uma ilha
eh_ilha(Cidade) :-
    \+ conectado(Cidade, _),
    \+ conectado(_, Cidade).

# encontrar uma ilha 
verifica_ilha(Cidades, Ilha) :-
    findall(Cidade, (conectado(Cidade, _); conectado(_, Cidade)), TodasCidades),
    list_to_set(TodasCidades, CidadesUnicas),
    member(Ilha, CidadesUnicas),
    eh_ilha(Ilha).
