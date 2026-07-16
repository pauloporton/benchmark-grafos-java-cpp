#include <vector>
#include <iostream>
#include <climits>

struct Aresta {

    int origem, destino, peso;

    Aresta(int u, int v, int p) {
        origem = u;
        destino = v;
        peso = p;
    }

    bool operator<(const Aresta& outra) const {
        return peso < outra.peso;
    }
};

bool bellmanford(std::vector<Aresta>& arestas, std::vector<int>& dist, int n, int origem) {
    dist[origem] = 0;
    for(int i = 1; i < n; i++) {
        for(const auto& aresta : arestas) {
            int u = aresta.origem;
            int v = aresta.destino;
            int p = aresta.peso;
            if(dist[u] != INT_MAX && dist[u] + p < dist[v]) {
                dist[v] = dist[u] + p;
            }
        }
    }
    for(const auto& aresta : arestas) {
        int u = aresta.origem;
        int v = aresta.destino;
        int p = aresta.peso;
        if(dist[u] != INT_MAX && dist[u] + p < dist[v]) {
            return true;
        }
    }
    return false;
}

void monta_arestas(std::vector<Aresta>& arestas) {
    arestas.push_back({1, 2, 2});
    arestas.push_back({1, 3, 9});
    arestas.push_back({1, 5, 7});
    arestas.push_back({2, 6, 6});
    arestas.push_back({6, 3, -3});
    arestas.push_back({6, 5, -2});
}

int main() {
    int n = 6;
    std::vector<Aresta> arestas;
    monta_arestas(arestas);
    std::vector<int> dist(n + 1, INT_MAX);
    if(!bellmanford(arestas, dist, n, 1)) {
        for(int i = 1; i <= n; i++) {
            if(dist[i] != INT_MAX) {
                std::cout << dist[i] << ' ';
            } else {
                std::cout << "Inalcançável ";
            }
        }
        std::cout << "\n";
    } else {
        std::cout << "Há ciclo(s) negativo(s) no grafo.\n";
    }
    return 0;
}

