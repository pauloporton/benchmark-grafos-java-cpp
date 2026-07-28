#include <benchmark/benchmark.h>
#include <fstream>
#include <queue>
#include <string>
#include <vector>

struct GrafoSemPeso {
    int V;
    int E;
    std::vector<std::pair<int, int>> arestas;
};

GrafoSemPeso carregarGrafoSemPeso(const std::string& caminho) {
    std::ifstream arquivo(caminho);
    if (!arquivo.is_open()) {
        throw std::runtime_error("Nao foi possivel abrir o arquivo: " + caminho);
    }

    GrafoSemPeso g;
    arquivo >> g.V >> g.E;
    g.arestas.reserve(g.E);

    for (int i = 0; i < g.E; i++) {
        int u, v;
        arquivo >> u >> v;
        g.arestas.emplace_back(u, v);
    }

    return g;
}

std::vector<std::vector<int>> montarListaAdjacencia(const GrafoSemPeso& g) {
    std::vector<std::vector<int>> adj(g.V + 1);
    for (const auto& [u, v] : g.arestas) {
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    return adj;
}

long long bfs_parcial(std::vector<std::vector<int>>& adj, int V, int origem, std::vector<bool>& visitados) {
    long long operacoes = 0;
    std::queue<int> fila;

    fila.push(origem);
    visitados[origem] = true;

    while(!fila.empty()) {
        int atual = fila.front();
        fila.pop();
        operacoes++;

        for(int vizinho : adj[atual]) {
            if(!visitados[vizinho]) {
                fila.push(vizinho);
                visitados[vizinho] = true;
            }
        }
    }

    return operacoes;
}

long long bfs_completo(std::vector<std::vector<int>>& adj, int V) {
    long long operacoes_total = 0;
    std::vector<bool> visitados(V + 1);
    
    for(int i = 1; i <= V; i++) {
        if(!visitados[i]) {
            operacoes_total += bfs_parcial(adj, V, i, visitados);
        }
    }

    return operacoes_total;
}

void registrarBenchmarksBFS() {
    const std::vector<std::string> casos = {"melhor", "pior", "esparso", "medio", "denso"};
    const std::vector<int> escalas = {10, 30, 100, 300, 1000, 3000, 10000, 30000, 100000};

    for (const auto& caso : casos) {
        for (int V : escalas) {
            std::string caminho = "../grafos/BFS/" + caso + "/" + std::to_string(V) + ".txt";
            std::string nome = "Teste_BFS_" + caso + "_" + std::to_string(V);

            benchmark::RegisterBenchmark(nome.c_str(), [caminho](benchmark::State& state) {
                GrafoSemPeso grafo;
                try {
                    grafo = carregarGrafoSemPeso(caminho);
                } catch (const std::exception& e) {
                    state.SkipWithError(e.what());
                    return;
                }
                auto adj = montarListaAdjacencia(grafo);

                long long operacoesUltimaExecucao = 0;

                for (auto _ : state) {
                    operacoesUltimaExecucao = bfs_completo(adj, grafo.V);
                    benchmark::DoNotOptimize(operacoesUltimaExecucao);
                }

                state.counters["V"] = grafo.V;
                state.counters["E"] = grafo.E;
                state.counters["operacoes"] = static_cast<double>(operacoesUltimaExecucao);
            });
        }
    }
}

int main(int argc, char** argv) {
    registrarBenchmarksBFS();

    benchmark::Initialize(&argc, argv);
    if (benchmark::ReportUnrecognizedArguments(argc, argv)) return 1;
    benchmark::RunSpecifiedBenchmarks();
    benchmark::Shutdown();

    return 0;
}
