package benchmark;

import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.StringTokenizer;

/**
 * Lê os arquivos de grafo gerados pelo gerador_grafos.py.
 *
 * Formato dos arquivos:
 *   linha 1:      V E
 *   linhas 2..E+1: "u v"      (grafos sem peso: BFS/DFS)
 *              ou "u v w"     (grafos com peso: Kruskal/BellmanFord)
 */
public class LeitorGrafo {

    // Representa uma aresta genérica lida do arquivo (com ou sem peso).
    public static class ArestaSimples {
        public final int origem;
        public final int destino;
        public final int peso;

        public ArestaSimples(int origem, int destino, int peso) {
            this.origem = origem;
            this.destino = destino;
            this.peso = peso;
        }
    }

    // Resultado da leitura: quantidade de vértices + lista de arestas cruas
    public static class GrafoLido {
        public final int v;
        public final List<ArestaSimples> arestas;

        public GrafoLido(int v, List<ArestaSimples> arestas) {
            this.v = v;
            this.arestas = arestas;
        }
    }

    // Lê um arquivo sem peso ("u v" por linha) e monta lista de adjacência (para BFS/DFS).
    public static List<List<Integer>> lerListaAdjacencia(String caminho) throws IOException {
        GrafoLido lido = lerBruto(caminho);

        List<List<Integer>> grafo = new ArrayList<>();
        for (int i = 0; i <= lido.v; i++) {
            grafo.add(new ArrayList<>());
        }

        for (ArestaSimples a : lido.arestas) {
            grafo.get(a.origem).add(a.destino);
            grafo.get(a.destino).add(a.origem);
        }

        return grafo;
    }

    // Lê um arquivo com peso ("u v w" por linha), usado por Kruskal e BellmanFord.
    public static GrafoLido lerArestasComPeso(String caminho) throws IOException {
        return lerBruto(caminho);
    }

    private static GrafoLido lerBruto(String caminho) throws IOException {
        try (BufferedReader br = Files.newBufferedReader(Paths.get(caminho))) {
            StringTokenizer cabecalho = new StringTokenizer(br.readLine());
            int v = Integer.parseInt(cabecalho.nextToken());
            int e = Integer.parseInt(cabecalho.nextToken());

            List<ArestaSimples> arestas = new ArrayList<>(e);
            for (int i = 0; i < e; i++) {
                String linha = br.readLine();
                StringTokenizer st = new StringTokenizer(linha);
                int u = Integer.parseInt(st.nextToken());
                int w = Integer.parseInt(st.nextToken());
                int peso = st.hasMoreTokens() ? Integer.parseInt(st.nextToken()) : 1;
                arestas.add(new ArestaSimples(u, w, peso));
            }

            return new GrafoLido(v, arestas);
        }
    }
}
