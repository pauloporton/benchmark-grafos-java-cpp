# benchmark-grafos-java-cpp

Projeto desenvolvido para a disciplina de Estrutura de Dados e Algoritmos do curso de Ciência da Computação da Universidade Federal de Campina Grande.

## Introdução

Java e C++ são duas linguagens de programação extremamente utilizadas nos mais diversos tipos de aplicações. Adotando abordagens distintas, C++ oferece um melhor controle de memória e tempo de execução, enquanto Java se destaca na portabilidade e acionamento automático do Garbage Collector. Na prática, o desempenho de um algoritmo pode ser diretamente impactado pela escolha da linguagem em que será implementado. Nesse projeto, iremos realizar um estudo comparativo de desempenho de algoritmos clássicos de grafos, avaliando sua eficiência na prática quando implementados nessas duas linguagens.

## Como rodar o experimento

### Dependências

**Linguagens**
- Java
- C++
- Python 3

**Bibliotecas**
- Maven
- Matplotlib
- Google Benchmark

### Comandos

```bash
# roda os testes
chmod +x run-benchmark.sh
nohup ./run-benchmark.sh > log_execucao.txt 2>&1 &

# verifica o progresso
tail -f log_execucao.txt

# verifica se ta rodando
ps aux | grep run-benchmark
```

## Metodologia

A pesquisa adotou uma abordagem experimental controlada, seguindo esses passos:

### Implementação dos grafos

Os vértices são apenas representados como inteiros, não guardando informações adicionais, a fim de simplificar a implementação dos testes. Cada inteiro é um identificador de um vértice que corresponde a sua ordem de inserção no grafo. Todos os grafos são 1-indexado. Nenhum dos grafos usados é garantidamente conectado.

Para grafos não ponderados e bidirecionais usados na BFS e DFS foram usadas listas de adjacência (listas de listas de inteiros) para a representação do grafo, sendo cada posição da lista a representação de um vértice e cada elemento dessa lista um vizinho do vértice correspondente.

Para grafos direcionados e ponderados foram usadas classes e estruturas de arestas, guardando o vértice de origem, vértice de destino e peso da aresta como inteiros. Para a representação dos grafos, foram usadas listas de arestas. A ausência de um vértice na lista de arestas não significa a inexistência dele no grafo, apenas indica a ausência de conexões com outros vértices, de fato, o grafo sempre possui a quantidade de vértices indicada no teste.

### Implementação dos algoritmos

- **DFS** - Implementação recursiva caminhando uma vez por todos os nós do grafo, mesmo com grafos desconectados. Evita caminhar por nós usados com um array de booleanos marcando os nós usados.
- **BFS** - Implementação iterativa usando uma Queue de nós para garantir o caminhamento em largura e array de booleanos marcando nós usados. Caminha por todos os nós do grafo mesmo que seja desconectado.
- **Kruskal** - Implementação gulosa ordenando a lista de arestas por seus pesos e escolhendo sempre a menor aresta disponível que não gera ciclos para adicionar na árvore. A implementação da Dsu usa um array de inteiros para representar os pais, sendo as raízes dos componentes representados por números negativos indicando a quantidade de vértices em seu componente e um inteiro representando o pai do vértice para os outros casos. Caso a quantidade de arestas necessária para formar uma árvore seja alcançada, o algoritmo é encerrado precocemente.
- **Bellman Ford** - Implementação dinâmica que percorre a lista de arestas V (quantidade de vértices) - 1 vezes atualizando as distâncias mínimas e verificando uma última vez para averiguar a existência de ciclos negativos. Caso uma iteração por todas as arestas aconteça sem que nenhuma distância seja atualizada, o algoritmo é encerrado precocemente, já que todas as distâncias mínimas foram encontradas.

Para melhor entendimento do funcionamento de cada algoritmo, verifique as versões didáticas dos códigos nas duas linguagens usadas no projeto no diretório `algoritmos`.

### Geração de entradas

A geração dos grafos foi feita por meio de um algoritmo na linguagem de programação Python, explorando 5 casos para cada algoritmo. Para os casos que testam densidades diferentes é importante ressaltar que os grafos não seguem a proporção em relação a densidade máxima de um grafo, isto é, V * (V-1). Ao invés disso, é usada uma proporção linear calculada empiricamente. Para entender melhor essa escolha e cálculo das proporções confira a seção "Dúvidas importantes e esclarecimentos".

**Tamanhos:** 10, 30, 100, 300, 1000, 3000, 10000, 30000, 100000

**Casos:** Melhor, Pressão, Esparso, Médio, Denso

- **Melhor caso** - Se refere a um grafo que estimula o melhor caso teórico de cada algoritmo, usado como base para controle e previsibilidade do experimento e comparação com outros casos.
- **Caso de pressão** - Se refere a grafos que estruturalmente pressionam as linguagens para evidenciar a diferença de performances, sem necessariamente forçar um pior caso teórico. Esses casos se aproximam mais de situações realistas de representações e armazenamento de grafos. Para entender melhor os casos de pressão para cada algoritmo confira a seção "Casos de teste".
- **Esparso** - Caso com poucas arestas em relação ao número de vértices, mais precisamente 10% da densidade máxima calculada.
- **Médio** - Caso com um número intermediário de arestas em relação ao número de vértices, mais precisamente 50% da densidade máxima calculada.
- **Denso** - Caso com muitas arestas em relação ao número de vértices, mais precisamente 90% da densidade máxima calculada.

### Ambientes de teste e análise dos resultados

Os testes foram rodados por meio de Benchmarks, utilizando as bibliotecas Google Benchmark para C++ e JMH (Java MicroBenchmark Harness) para Java, que mediram tempo de execução médio e pico de memória para cada caso de cada algoritmo variando o tamanho das entradas. Os resultados foram transferidos para arquivos `.json` que foram então interpretados por um script em Python com o uso da biblioteca Matplotlib para montar a representação visual dos gráficos. Para cada teste foram realizadas 3 rodadas de aquecimento e 7 execuções para Java e 7 execuções para C++ sem rodadas de aquecimento.

## Casos de teste

### DFS

- **Melhor caso** - Árvore binária balanceada; a árvore binária balanceada permite que a altura da árvore permaneça no máximo em "logV 2" (formatar dps), o que faz com que para a maior entrada com 10^5 vértices, a altura máxima seja 17, o que mantém a pilha de recursão com uma quantidade pequena de vértices, otimizando todo o processo.
- **Caso de pressão** - Grafo Linear; o grafo linear faz com que, para o maior número de vértices, o primeiro vértice esteja a 99.999 arestas de distância do último, estressando ao máximo o jeito que as linguagens tratam seus limites de chamadas recursivas. Exemplo realista: Sequência de edições em um arquivo de texto.

### BFS

- **Melhor caso** - Grafo linear; o grafo linear permite que a fila da BFS armazene apenas um vértice simultaneamente, já que cada vértice só possui um vizinho não usado ainda. Isso otimiza o uso de memória e operações da fila.
- **Caso de pressão** - Árvore binária balanceada; na árvore balanceada, os níveis mais baixos possuem muitos vértices, logo a fila precisa armazenar muitos elementos de uma vez no final da execução. Para o maior tamanho da entrada isso seria cerca de 500.000 vértices. Esse cenário testa a otimização de armazenamento em estruturas de dados para ambas as linguagens. Exemplo realista: Árvore de arquivos e diretórios em um computador.

### Kruskal

- **Melhor caso** - Árvore binária balanceada ordenada; este grafo gera uma lista de arestas já ordenadas, não sendo gasto tempo com a ordenação e após o percorrimento de todas as arestas, a árvore fica pronta encerrando a execução no menor tempo possível.
- **Caso de pressão** - Grafo fragmentado; esse grafo simula diversos grafos desconectados de tamanhos distintos, gerando um grau de desordem e forçando a DSU a não comprimir todos os caminhos rapidamente para evidenciar a diferença entre as linguagens. Exemplo realista: Grafo de seguidores em redes sociais, com alguns pontos servindo como hubs com grandes quantidades de vértices.

### Bellman Ford

- **Melhor caso** - Árvore binária balanceada; ao aplicar o algoritmo nesse grafo, todos os menores caminhos a partir da raiz serão encontrados em apenas uma iteração, já que só há como alcançar cada vértice por um caminho a partir da raiz de uma árvore, logo, na segunda iteração o algoritmo não realizará nenhuma troca encerrando a execução precocemente.
- **Caso de pressão** - Grafo matriz invertido; esse grafo se trata de uma matriz saindo do vértice 1x1 e construindo ligações para a direita e para baixo com os próximos vértices. A execução é realizada saindo da última aresta até alcançar a primeira, garantindo que o algoritmo não irá se encerrar em apenas uma iteração. Esse cenário simula uma matriz em que há diversos caminhos para sair de um nó e chegar em outro, testando o armazenamento da estrutura e performance em ambas as linguagens. Exemplo realista: Casas em um jogo de tabuleiro.

Os casos esparsos, médios e densos são estruturalmente iguais para todos os algoritmos, com a única diferença sendo a adição de pesos aleatoriamente com valores entre -300 e 1000 para os casos de Kruskal e Bellman Ford. A quantidade de arestas para cada grafo é obtida através da fórmula explicada na seção "Dúvidas importantes e esclarecimentos" e as arestas também são geradas aleatoriamente da seguinte forma: enquanto o número exigido de arestas não foi alcançado, dois vértices aleatórios são selecionados. Caso não haja uma aresta entre eles ainda, a conexão é feita e adicionada na lista de arestas. Esse processo se repete até que seja obtido o número necessário de arestas.

## Hipótese teórica

Com base nos estudos teóricos feitos a partir das diferenças entre Java e C++ e das implementações dos quatro algoritmos de grafos, fizemos as seguintes previsões:

1. Em todos os algoritmos, o tempo de execução da implementação em C++ tende a ser mais rápido do que a de Java.
2. Para um número de vértices muito grande, a DFS em Java tende a "estourar".
3. Nas implementações em Java, o pico de memória será maior nas primeiras repetições, visto que terá as alocações de memória para o garbage collector.

## Análise dos resultados

## Ameaças à validade do experimento

1. **Hardware e heap** - Em alguns casos, como DFS denso, esparso e médio, a implementação em Java não apresentou resultados ao se aproximar de 10⁴ vértices, prejudicando a comparação nesses cenários.
2. **Quantidade de repetições** - Cada caso de algoritmo foi repetido 7 vezes para a métrica de tempo de execução e 1 vez para medir o pico de memória, o que pode causar distorções.
3. Como os grafos são gerados de forma controlada, o experimento pode não refletir com grafos usados na realidade.
4. Não foram testados grafos com densidade máxima.

## Conclusão

## Referências

- https://roadmap.sh/java/vs-cpp
- https://cp-algorithms.com/
