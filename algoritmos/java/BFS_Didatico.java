package algoritmos.java;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;

/*
 * Implementação da busca em largura (BFS).
 * O algoritmo percorre todos os vértices do grafo.
 */
public class BFS_Didatico {

    public static void main(String[] args) {

        // Número de vértices
        int n = 6;

        // Cria a lista de adjacência do grafo
        List<List<Integer>> grafo = new ArrayList<>();
        for (int i = 0; i <= n; i++) {
            grafo.add(new ArrayList<>());
        }

        montaGrafo(grafo);

        // Armazena a ordem em que os vértices foram visitados
        List<Integer> caminho = new ArrayList<>();

        // Marca quais vértices já foram visitados
        boolean[] usados = new boolean[n + 1];

        // Executa a BFS em cada componente do grafo
        for (int i = 1; i <= n; i++) {
            if (!usados[i]) {
                bfs(grafo, caminho, usados, i);
            }
        }

        // Imprime a ordem de visita
        for (int no : caminho) {
            System.out.print(no + " ");
        }
        System.out.println();
    }

    // Adiciona as arestas do grafo
    public static void montaGrafo(List<List<Integer>> grafo) {

        grafo.get(1).add(3);
        grafo.get(3).add(1);

        grafo.get(1).add(2);
        grafo.get(2).add(1);

        grafo.get(3).add(4);
        grafo.get(4).add(3);

        grafo.get(2).add(3);
        grafo.get(3).add(2);

        grafo.get(5).add(6);
        grafo.get(6).add(5);
    }

    // Realiza a busca em largura a partir de um vértice
    public static void bfs(List<List<Integer>> grafo, List<Integer> caminho, boolean[] usados, int origem) {

        // Fila utilizada pela BFS
        Queue<Integer> fila = new LinkedList<>();

        fila.add(origem);
        usados[origem] = true;

        while (!fila.isEmpty()) {

            // Remove o primeiro elemento da fila
            int atual = fila.poll();
            caminho.add(atual);

            // Adiciona na fila os vizinhos ainda não visitados
            for (int vizinho : grafo.get(atual)) {
                if (!usados[vizinho]) {
                    fila.add(vizinho);
                    usados[vizinho] = true;
                }
            }
        }
    }
}
