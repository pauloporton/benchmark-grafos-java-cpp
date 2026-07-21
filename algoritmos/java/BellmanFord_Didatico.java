package algoritmos.java;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class BellmanFord_Didatico {
    public static void main(String[] args) {
        int n = 6;
        List<Aresta> arestas = new ArrayList<>();
        montaArestas(arestas);

        int[] dist = new int[n+1];

        if (!bellmanFord(arestas, dist, n, 1)) {
            for (int i = 1; i <= n; i++) {
                if (dist[i] != Integer.MAX_VALUE / 2) {
                    System.out.println(dist[i] + " ");
                } else {
                    System.out.println("Inalcançavel ");
                }
            }
            System.out.println();
        } else {
            System.out.println("Há ciclo(s) negativo(s) no grafo.");
        }
    }

    public static class Aresta {
        int origem;
        int destino;
        int peso;

        public Aresta(int origem, int destino, int peso) {
            this.origem = origem;
            this.destino = destino;
            this.peso = peso;
        }
    }

    public static void montaArestas(List<Aresta> arestas) {
        arestas.add(new Aresta(1, 2, 2));
        arestas.add(new Aresta(1, 3, 9));
        arestas.add(new Aresta(1, 5, 7));
        arestas.add(new Aresta(2, 6, 6));
        arestas.add(new Aresta(6, 3, -3));
        arestas.add(new Aresta(6, 5, -2));
    }

    public static boolean bellmanFord(List<Aresta> arestas, int[] dist, int n, int origem) {
        Arrays.fill(dist, Integer.MAX_VALUE / 2);
        dist[origem] = 0;

        for (int i = 1; i < n; i++) {
            for (Aresta aresta : arestas) {
                int u = aresta.origem;
                int v = aresta.destino;
                int p = aresta.peso;

                if (dist[u] != Integer.MAX_VALUE / 2 && dist[u] + p < dist[v]) {
                    dist[v] = dist[u] + p;
                }
            }
        }

        for (Aresta aresta : arestas) {
            int u = aresta.origem;
            int v = aresta.destino;
            int p = aresta.peso;
            
            if (dist[u] != Integer.MAX_VALUE / 2 && dist[u] + p < dist[v]) {
                return true; 
            }
        }
        return false;

    }

}
