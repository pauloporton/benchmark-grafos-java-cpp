#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>

struct Dsu {

    std::vector<int> pais;

    Dsu(int n) {
        pais = std::vector<int>(n + 1, -1);
    }

    int find(int a) {
        if(pais[a] < 0) return a;
        pais[a] = find(pais[a]);
        return pais[a];
    }

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

struct Aresta {
    int origem, destino, peso;

    Aresta(int o, int d, int p) {
        origem = o;
        destino = d;
        peso = p;
    }

    bool operator< (const Aresta& outra) const {
        return peso < outra.peso;
    }

};

int kruskal(std::vector<Aresta>& arestas, std::vector<Aresta>& arvore, int n) {
    sort(arestas.begin(), arestas.end());
    Dsu dsu(n);
    int peso_total = 0;
    for(Aresta& a : arestas) {
        if(dsu.uni(a.origem, a.destino)) {
            arvore.push_back(a);
            peso_total += a.peso;
            if(arvore.size() == n-1)
                break;
        }
    }
    if(arvore.size() == n - 1) {
        return peso_total;
    }
    return INT_MAX;
}

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
    int n = 7;
    std::vector<Aresta> arestas;
    monta_arestas(arestas);
    std::vector<Aresta> arvore;
    int p = kruskal(arestas, arvore, n);
    if(p != INT_MAX) {
        std::cout << p << "\n";
    } else {
        std::cout << "Não foi possível montar uma árvore a partir das arestas fornecidas.\n";
    }

    return 0;
}

