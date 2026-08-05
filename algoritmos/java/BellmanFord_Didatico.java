package algoritmos.java;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/*
 * Implementação do algoritmo de Bellman-Ford.
 * O algoritmo calcula a menor distância a partir de um vértice de origem.
 */
public class BellmanFord_Didatico {

    public static void main(String[] args) {

        // Número de vértices
        int n = 6;

        // Lista de arestas do grafo
        List<Aresta> arestas = new ArrayList<>();
        montaArestas(arestas);

        // Vetor que armazena as menores distâncias
        int[] dist = new int[n + 1];

        // Executa o algoritmo
        if (!bellmanFord(arestas, dist, n, 1)) {

            // Exibe as distâncias encontradas
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

    // Adiciona as arestas do grafo
    public static void montaArestas(List<Aresta> arestas) {

        arestas.add(new Aresta(1, 2, 2));
        arestas.add(new Aresta(1, 3, 9));
        arestas.add(new Aresta(1, 5, 7));
        arestas.add(new Aresta(2, 6, 6));
        arestas.add(new Aresta(6, 3, -3));
        arestas.add(new Aresta(6, 5, -2));
    }

    // Executa o algoritmo de Bellman-Ford
    public static boolean bellmanFord(List<Aresta> arestas, int[] dist, int n, int origem) {

        // Inicializa todas as distâncias
        Arrays.fill(dist, Integer.MAX_VALUE / 2);
        dist[origem] = 0;

        // Relaxa todas as arestas
        for (int i = 1; i < n; i++) {

            boolean atualizou = false;

            for (Aresta aresta : arestas) {

                int u = aresta.origem;
                int v = aresta.destino;
                int p = aresta.peso;

                if (dist[u] != Integer.MAX_VALUE / 2 && dist[u] + p < dist[v]) {
                    dist[v] = dist[u] + p;
                    atualizou = true;
                }
            }

            // Encerra caso nenhuma distância tenha sido alterada
            if (!atualizou) {
                break;
            }
        }

        // Verifica se existe ciclo de peso negativo
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
