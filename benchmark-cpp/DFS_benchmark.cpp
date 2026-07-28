#include <benchmark/benchmark.h>
#include <fstream>
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

long long dfs_parcial(std::vector<std::vector<int>>& adj, int V, int atual, std::vector<bool>& visitados) {
    long long operacoes = 0;
    visitados[atual] = true;
    for(int vizinho : adj[atual]) {
        if(!visitados[vizinho]) {
            operacoes += dfs_parcial(adj, V, vizinho, visitados);
        }
    }
    return operacoes + 1;
}

long long dfs_completo(std::vector<std::vector<int>>& adj, int V) {
    long long operacoes_total = 0;
    std::vector<bool> visitados(V + 1);
    
    for(int i = 1; i <= V; i++) {
        if(!visitados[i]) {
            operacoes_total += dfs_parcial(adj, V, i, visitados);
        }
    }

    return operacoes_total;
}

void registrarBenchmarksDFS() {
    const std::vector<std::string> casos = {"melhor", "pior", "esparso", "medio", "denso"};
    const std::vector<int> escalas = {10, 30, 100, 300, 1000, 3000, 10000, 30000, 100000};

    for (const auto& caso : casos) {
        for (int V : escalas) {
            std::string caminho = "../grafos/DFS/" + caso + "/" + std::to_string(V) + ".txt";
            std::string nome = "Teste_DFS_" + caso + "_" + std::to_string(V);

            benchmark::RegisterBenchmark(nome.c_str(), [caminho, V](benchmark::State& state) {
                const int LIMITE_RECURSAO_CONHECIDO = 70000;
                if (V > LIMITE_RECURSAO_CONHECIDO) {
                    state.SkipWithError("V acima do limite de recursao conhecido para DFS (stack overflow esperado)");
                    return;
                }

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
                    operacoesUltimaExecucao = dfs_completo(adj, grafo.V);
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
    registrarBenchmarksDFS();

    benchmark::Initialize(&argc, argv);
    if (benchmark::ReportUnrecognizedArguments(argc, argv)) return 1;
    benchmark::RunSpecifiedBenchmarks();
    benchmark::Shutdown();

    return 0;
}
