package benchmark;

import algoritmos.java.DFS_Didatico;
import org.openjdk.jmh.annotations.*;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;

@BenchmarkMode(Mode.AverageTime) //Tempo médio por operação
@OutputTimeUnit(TimeUnit.MICROSECONDS) //Unidade de tempo do resultado (microssegundos)
@Warmup(iterations = 3, time = 1, timeUnit = TimeUnit.SECONDS) // 3 iterações de aquecimento durando 1 segundo cada
@Measurement(iterations = 5, time = 1, timeUnit = TimeUnit.SECONDS) // 5 iterações após o aquecimento que vão contar pro resultado (valor final é a média das 5)
@Fork(1)
@State(Scope.Benchmark)
public class DFSBenchmark {

    // Tipos de caso
    @Param({"melhor", "pior", "esparso", "medio", "denso"})
    public String caso;

    // Número de vertíces
    @Param({"10", "30", "100", "300", "1000", "3000", "10000", "30000", "100000"})
    public String tamanho;

    // Variáveis internas
    private List<List<Integer>> grafo;

    // Setup executado 1 vez por combinação de caso/tamanho antes dos aquecimentos e medições
    @Setup(Level.Trial)
    public void setup() throws Exception {
        String caminho = "../grafos/DFS/" + caso + "/" + tamanho + ".txt";
        grafo = LeitorGrafo.lerListaAdjacencia(caminho);
    }

    // Benchmark (por ter o return, a jmh já previne a eliminação de "código morto")
    @Benchmark
    public List<Integer> benchmarkDFS() {
        int n = grafo.size() - 1;
        List<Integer> caminhoPercorrido = new ArrayList<>();
        boolean[] usados = new boolean[n + 1];

        for (int i = 1; i <= n; i++) {
            if (!usados[i]) {
                DFS_Didatico.dfs(grafo, caminhoPercorrido, usados, i);
            }
        }
        return caminhoPercorrido;
    }
}
