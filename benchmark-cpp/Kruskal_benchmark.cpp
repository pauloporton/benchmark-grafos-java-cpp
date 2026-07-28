#include <benchmark/benchmark.h>
#include <fstream>
#include <string>
#include <vector>

struct Aresta {
    int u, v, peso;

    Aresta(int u, int v, int peso) : u(u), v(v), peso(peso) {}

    bool operator< (const Aresta& outra) const {
         return peso < outra.peso;
    }
};

struct GrafoComPeso {
    int V;
    int E;
    std::vector<Aresta> arestas;
};


GrafoComPeso carregarGrafoComPeso(const std::string& caminho) {
    std::ifstream arquivo(caminho);
    if (!arquivo.is_open()) {
        throw std::runtime_error("Nao foi possivel abrir o arquivo: " + caminho);
    }

    GrafoComPeso g;
    arquivo >> g.V >> g.E;
    g.arestas.reserve(g.E);

    for (int i = 0; i < g.E; i++) {
        int u, v, peso;
        arquivo >> u >> v >> peso;
        g.arestas.emplace_back(Aresta{u, v, peso});
    }

    return g;
}

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

std::pair<long long, long long> kruskal(std::vector<Aresta>& arestas, int V, int origem) {
    long long operacoes = 0;
    long long peso_total = 0;

    sort(arestas.begin(), arestas.end());
    Dsu d(V);
    
    std::vector<Aresta> arvore;
    for(Aresta& aresta: arestas) {
        operacoes++;
        if(d.uni(aresta.u, aresta.v)) {
            peso_total += aresta.peso;
            arvore.push_back(aresta);
            if(arvore.size() == V - 1) {
                break;
            }
        }
    }

    return {operacoes, peso_total};
}

void registrarBenchmarksKruskal() {
    const std::vector<std::string> casos = {"melhor", "pior", "esparso", "medio", "denso"};
    const std::vector<int> escalas = {10, 30, 100, 300, 1000, 3000, 10000, 30000, 100000};

    for (const auto& caso : casos) {
        for (int V : escalas) {
            std::string caminho = "../grafos/Kruskal/" + caso + "/" + std::to_string(V) + ".txt";
            std::string nome = "Teste_Kruskal_" + caso + "_" + std::to_string(V);

            benchmark::RegisterBenchmark(nome.c_str(), [caminho](benchmark::State& state) {
                GrafoComPeso grafo;
                try {
                    grafo = carregarGrafoComPeso(caminho);
                } catch (const std::exception& e) {
                    state.SkipWithError(e.what());
                    return;
                }
                long long operacoesUltimaExecucao = 0;
                long long peso_arvore = 0;

                for (auto _ : state) {
                    auto resultado = kruskal(grafo.arestas, grafo.V, 1);
                    operacoesUltimaExecucao = resultado.first;
                    peso_arvore = resultado.second;
                    benchmark::DoNotOptimize(operacoesUltimaExecucao);
                }

                state.counters["V"] = grafo.V;
                state.counters["E"] = grafo.E;
                state.counters["operacoes"] = static_cast<double>(operacoesUltimaExecucao);
                state.counters["peso_arvore"] = static_cast<double>(peso_arvore);
            });
        }
    }
}

int main(int argc, char** argv) {
    registrarBenchmarksKruskal();

    benchmark::Initialize(&argc, argv);
    if (benchmark::ReportUnrecognizedArguments(argc, argv)) return 1;
    benchmark::RunSpecifiedBenchmarks();
    benchmark::Shutdown();

    return 0;
}
