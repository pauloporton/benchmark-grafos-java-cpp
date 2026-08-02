#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>

//Estrutura Dsu que guarda os pais de cada nó e caso o nó seja a raiz, guarda um valor negativo indicando quantos nós existem em seu componente
struct Dsu {

    std::vector<int> pais;
    //construtor que gurada n + 1 posições por ser 1-indexado, incialmente todos os nós são raízes de um componente unitário
    Dsu(int n) {
        pais = std::vector<int>(n + 1, -1);
    }
    //acha e atualiza por path compression os pais de um nó passado como parâmetro.
    int find(int a) {
        if(pais[a] < 0) return a;
        pais[a] = find(pais[a]);
        return pais[a];
    }
    //une dois componentes do grafo em um só, escolhendo um dos nós para ser a nova raiz
    bool uni(int a, int b) {
        a = find(a);
        b = find(b);

        if(a == b) return false;
        if(pais[a] < pais[b]) {
            pais[a] += pais[b];
            pais[b] = a;
        } else {
            pais[b] += pais[a];
            pais[a] = b;
        }
        return true;
    }
};
//Estrutura de aresta direcionada e ponderada que guarda o nó de origem, o destino e o peso da aresta
struct Aresta {
    int origem, destino, peso;

    Aresta(int u, int v, int p) {
        origem = u;
        destino = v;
        peso = p;
    }
    //define que uma aresta é menor que outra se seu peso é menor, necessário para a ordenação do vetor de arestas
    bool operator< (const Aresta& outra) const {
        return peso < outra.peso;
    }

};

int kruskal(std::vector<Aresta>& arestas, std::vector<Aresta>& arvore, int n) {
    //ordena as arestas pelo peso
    sort(arestas.begin(), arestas.end());
    //inicializa a Dsu com tamanho n
    Dsu dsu(n);
    int peso_total = 0;
    //Passa por todas as arestas conferindo se a adição de cada uma na árvore gera ciclo, caso contrário adiciona
    for(const auto& a : arestas) {
        if(dsu.uni(a.origem, a.destino)) {
            arvore.push_back(a);
            peso_total += a.peso;
            //caso o número de arestas alcance n-1, todos os nós já estão ligados, portanto é possível encerrar precocemente
            if(arvore.size() == n-1)
                break;
        }
    }
    if(arvore.size() == n - 1) {
        return peso_total;
    }
    return INT_MAX;
}
//Função que monta as arestas com valores fixos, caso queira testar seu próprio grafo, altere esses valores
//O formato da aresta é ({origem, destino, peso})
void monta_arestas(std::vector<Aresta>& arestas) {
    arestas.push_back({1, 2, 1});
    arestas.push_back({1, 5, 3});
    arestas.push_back({1, 7, 6});
    arestas.push_back({2, 3, 2});
    arestas.push_back({2, 4, 8});
    arestas.push_back({3, 5, 4});
    arestas.push_back({4, 6, 10});
    arestas.push_back({5, 6, 9});
    arestas.push_back({5, 7, 5});
    arestas.push_back({7, 3, 11});
}

int main() {
    //grafo com 7 nós
    int n = 7;
    std::vector<Aresta> arestas;
    monta_arestas(arestas);
    std::vector<Aresta> arvore;
    int p = kruskal(arestas, arvore, n);
    //imprime o custo total da árvore se foi possível gerá-la
    if(p != INT_MAX) {
        std::cout << p << "\n";
    } else {
        std::cout << "Não foi possível montar uma árvore a partir das arestas fornecidas.\n";
    }

    return 0;
}

