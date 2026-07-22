package algoritmos.java;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;

public class BFS_Didatico {
    public static void main(String[] args) {
        int n = 6;

        List<List<Integer>> grafo = new ArrayList<>();
        for (int i = 0; i <= n; i++) {
            grafo.add(new ArrayList<>());
        }
        montaGrafo(grafo);

        List<Integer> caminho = new ArrayList<>();
        boolean[] usados = new boolean[n + 1];

        for (int i = 1; i <= n; i++) {
            if (!usados[i]) {
                bfs(grafo, caminho, usados, i);
            }
        }

        for (int no : caminho) {
            System.out.print(no + " ");
        }
        System.out.println();
    }

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

    public static void bfs(List<List<Integer>> grafo, List<Integer> caminho, boolean[] usados, int origem) {
        Queue<Integer> fila = new LinkedList<>();
        fila.add(origem);
        usados[origem] = true;

        while (!fila.isEmpty()) {
            int atual = fila.poll();
            caminho.add(atual);

            for (int vizinho : grafo.get(atual)) {
                if (!usados[vizinho]) {
                    fila.add(vizinho);
                    usados[vizinho] = true;
                }
            }
        }
    }
}
