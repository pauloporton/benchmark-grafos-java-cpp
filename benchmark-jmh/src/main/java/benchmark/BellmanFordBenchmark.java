package benchmark;

import algoritmos.java.Aresta;
import algoritmos.java.BellmanFord_Didatico;
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
public class BellmanFordBenchmark {

    // Tipos de caso
    @Param({"melhor", "pior", "esparso", "medio", "denso"})
    public String caso;

    // Número de vertices
    @Param({"10", "30", "100"})
    public String tamanho;

    // Variáveis internas
    private List<Aresta> arestas;
    private int n;

    // Setup executado 1 vez por combinação de caso/tamanho antes dos aquecimentos e medições
    @Setup(Level.Trial)
    public void setup() throws Exception {
        String caminho = "../grafos/BellmanFord/" + caso + "/" + tamanho + ".txt";
        LeitorGrafo.GrafoLido lido = LeitorGrafo.lerArestasComPeso(caminho);

        n = lido.v;
        arestas = new ArrayList<>(lido.arestas.size());
        for (LeitorGrafo.ArestaSimples a : lido.arestas) {
            arestas.add(new Aresta(a.origem, a.destino, a.peso));
        }
    }

    // Benchmark (por adicionar o return, a jmh já previne a eliminação de "código morto")
    @Benchmark
    public int[] benchmarkBellmanFord() {
        int[] dist = new int[n + 1];
        BellmanFord_Didatico.bellmanFord(arestas, dist, n, 1);
        return dist;
    }
}
