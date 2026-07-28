#include <benchmark/benchmark.h>
#include <fstream>
#include <string>
#include <vector>
#include <climits>

struct Aresta {
    int u, v, peso;

    Aresta(int u, int v, int peso) : u(u), v(v), peso(peso) {}
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
        g.arestas.push_back(Aresta{u, v, peso});
    }

    return g;
}

std::pair<long long, bool> bellmanFord(std::vector<Aresta>& arestas, int V, int origem) {
    long long operacoes = 0;
    bool ciclo_negativo = false;
    std::vector<long long> dist(V + 1, LLONG_MAX);
    dist[origem] = 0;
    for(int i = 1; i < V; i++) {
        bool atualizou = false;
        for(const auto& aresta : arestas) {
            operacoes++;
            int u = aresta.u;
            int v = aresta.v;
            int p = aresta.peso;
            if(dist[u] != LLONG_MAX && dist[u] + p < dist[v]) {
                dist[v] = dist[u] + p;
                atualizou = true;
            }
        }
        if(!atualizou)
            break;
     }

     for(const auto& aresta : arestas) {
         int u = aresta.u;
         int v = aresta.v;
         int p = aresta.peso;
         if(dist[u] != LLONG_MAX && dist[u] + p < dist[v]) {
             ciclo_negativo = true;
             break;
         }
     }
    return {operacoes, ciclo_negativo};
}

void registrarBenchmarksBellmanFord() {
    const std::vector<std::string> casos = {"melhor", "pior", "esparso", "medio", "denso"};
    const std::vector<int> escalas = {10, 30, 100, 300, 1000, 3000, 10000, 30000, 100000};

    for (const auto& caso : casos) {
        for (int V : escalas) {
            std::string caminho = "../grafos/BellmanFord/" + caso + "/" + std::to_string(V) + ".txt";
            std::string nome = "Teste_Bellman_Ford_" + caso + "_" + std::to_string(V);

            benchmark::RegisterBenchmark(nome.c_str(), [caminho](benchmark::State& state) {
                GrafoComPeso grafo;
                try {
                    grafo = carregarGrafoComPeso(caminho);
                } catch (const std::exception& e) {
                    state.SkipWithError(e.what());
                    return;
                }
                long long operacoesUltimaExecucao = 0;
                bool ciclo_negativo = false;

                for (auto _ : state) {
                    auto resultado = bellmanFord(grafo.arestas, grafo.V, 1);
                    operacoesUltimaExecucao = resultado.first;
                    ciclo_negativo = resultado.second;
                    benchmark::DoNotOptimize(operacoesUltimaExecucao);
                }

                state.counters["V"] = grafo.V;
                state.counters["E"] = grafo.E;
                state.counters["operacoes"] = static_cast<double>(operacoesUltimaExecucao);
                state.counters["teve_ciclo_negativo"] = ciclo_negativo ? 1.0 : 0.0;
            });
        }
    }
}

int main(int argc, char** argv) {
    registrarBenchmarksBellmanFord();

    benchmark::Initialize(&argc, argv);
    if (benchmark::ReportUnrecognizedArguments(argc, argv)) return 1;
    benchmark::RunSpecifiedBenchmarks();
    benchmark::Shutdown();

    return 0;
}
