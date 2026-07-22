package algoritmos.java;

import java.util.ArrayList;
import java.util.List;

public class DFS_Didatico {
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
                dfs(grafo, caminho, usados, i);
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

    public static void dfs(List<List<Integer>> grafo, List<Integer> caminho, boolean[] usados, int no) {
        usados[no] = true;
        caminho.add(no);

        for (int vizinho : grafo.get(no)) {
            if (!usados[vizinho]) {
                dfs(grafo, caminho, usados, vizinho);
            }
        }
    }
}
