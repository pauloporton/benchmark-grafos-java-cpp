package benchmark;

import algoritmos.java.Aresta;
import algoritmos.java.Kruskal_Didatico;
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
public class KruskalBenchmark {

    // Tipos de caso
    @Param({"melhor", "pior", "esparso", "medio", "denso"})
    public String caso;

    // Número de vertices
    @Param({"10", "30", "100", "300", "1000", "3000", "10000", "30000", "100000"})
    public String tamanho;

    // Variáveis internas
    private List<Aresta> arestas;
    private int n;

    // Setup executado 1 vez por combinação de caso/tamanho antes dos aquecimentos e medições
    @Setup(Level.Trial)
    public void setup() throws Exception {
        String caminho = "../grafos/Kruskal/" + caso + "/" + tamanho + ".txt";
        arestas = LeitorGrafo.lerArestas(caminho);
        n = LeitorGrafo.lerNumeroVertices(caminho);
    }

    // Benchmark (por ter o return, a jmh já previne a eliminação de "código morto")
    @Benchmark
    public int benchmarkKruskal() {
        // A lista precisa ser recriada a cada execução porque nossa implementação de kruskal ordena arestas e monta arvore com efeitos colaterais.
        List<Aresta> copia = new ArrayList<>(arestas);
        List<Aresta> arvore = new ArrayList<>();
        return Kruskal_Didatico.kruskal(copia, arvore, n);
    }
}
