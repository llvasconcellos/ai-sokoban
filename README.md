# ai-sokoban
Artificial Intelligence Sokoban Solver with Python 

[![Sokoban Solver](https://img.youtube.com/vi/2BAlavTWj0Q/0.jpg)](https://www.youtube.com/watch?v=2BAlavTWj0Q)


# Introdução
Sokoban é um vídeo game de quebra cabeça e o objetivo é empurrar caixas do ponto de origem ao ponto destino em um armazém em forma de labirinto.
A intenção desta pesquisa é demonstrar a implementação de algoritmos de inteligência artificial para a resolução do problema.
O armazém (labirinto) é representado por uma matriz com posições [x,y] onde em cada posição está associado ou uma parede, espaço em branco, caixas, objetivos e o agente (sokoban). O agente é único.
O ambiente deste problema é estático, completamente observável, determinístico e sequencial. Os estados são discretos.

# Abordagem
Analisando o problema descrito, o espaço de estados é muito grande, podendo variar de acordo com o tamanho do labirinto e quantidade de caixas e objetivos, portanto a utilização de algoritmos de sem informação podem levar muito tempo e ter um custo computacional grande.
A estratégia de abordagem foi a utilização um algoritmo de busca em árvore A* e um agente baseado em objetivos. 
A estratégia de comparação de custos leva em consideração o custo uniforme, determinado pela distância real entre uma posição e outra, e uma função heurística que procura encontrar a menor distância entre a posição atual e objetivos.
Esta estratégia garante um tempo de execução menor encontrando a solução mais rapidamente.

# Metodologia
Para modelar o problema foi implementado uma entrada por forma de arquivo de texto onde estão definidos o labirinto, as posições originais das caixas e as posições objetivos, bem como a posição inicial do agente.
Foi desenvolvida uma aplicação em python usando janelas onde é possível carregar o arquivo de entrada do labirinto onde após sua leitura a aplicação considera o resultado desta leitura como o estado inicial.
É possível ver o algoritmo em ação no seguinte vídeo: https://youtu.be/DDCz2QoXH-A

Fig. 1 – Screenshots dos movimentos na resolução do problema

Os estados são representados por nós em uma árvore de busca onde cada nó contém as posições do agente e caixas no plano cartesiano (labirinto), além dos custos e direção.
O estado inicial contém as posições iniciais do agente e caixas e o estado final as caixas na posição objetivo.
As ações são movimentos em 4 direções (norte, sul, leste e oeste) e com um custo associado a ação que leva ao estado sucessor.
A deliberação é finalizada quando todas as caixas estão nas posições objetivo.
A aplicação gera um relatório com os resultados da busca como nós gerados, nós descartados, custos etempo de execução. 
Estes resultados serão comparados para análise de desempenho dos algoritmos de custo fixo e A*.
Algoritimo: busca(inicio, fim)
```
listaAberta <- posição inicial
enquanto conjuntoAberto não vazio faça
    no <- Remova do o elemento do topo da lista
    se no é objetivo final:
        termine
    senão
        sucessores <- encontarNosSucessores()
        para cada sucessores faca
            avaliação de custos
            encontrar próximo estado
            adicionar na listaAberta
retorna nos
```

# Resultado
Após a execução foi possível observar os seguintes resultados:

| Algoritmo      | Custo | Profundidade | Nós na Árvore | Nós Descartados | Total Nós | Tempo de Execução (s) |
|----------------|-------|--------------|---------------|-----------------|-----------|-----------------------|
| A*             | 21,29 | 20           | 38.867        | 170.699         | 578.922   | 88,75                 |
| Custo Uniforme | 21,3  | 20           | 22.212        | 897.682         | 2.608.110 | 380,51                |

# Conclusão
Após a implementação dos diferentes algoritmos para a resolução do problema foi possível evidenciar que apesar de ambos apresentarem uma solução ótima para o problema com movimentos parecidos a diferença foi em performance do algoritmo com uma diferença significativa no tempo de execução e custo computacional.
Os mesmos algoritmos podem ser aplicados em outros tipos de inteligência artificial para jogos, mas depende muito do tamanho do ambiente.
Quanto maior o ambiente mais custo computacional e tempo de execução.
Os próximos passos seriam a melhoria da função heurística tentando fórmulas diferentes.
É possível implementar também verificação de deadlocks e também, muito comum nesse tipo de implementação é a detecção de túnel onde é possível fazer o “pulo” de uma posição no início do túnel para o final do túnel economizando assim custo computacional.
