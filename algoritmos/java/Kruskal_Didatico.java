package algoritmos.java;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

/*
 * Implementação do algoritmo de Kruskal.
 * O objetivo é encontrar a Árvore Geradora Mínima de um grafo.
 */
public class Kruskal_Didatico {

    public static void main(String[] args) {
        // Número de vértices do grafo
        int n = 7;

        // Lista de arestas do grafo
        List<Aresta> arestas = new ArrayList<>();
        montaArestas(arestas);

        // Lista que armazenará a árvore geradora mínima
        List<Aresta> arvore = new ArrayList<>();

        int p = kruskal(arestas, arvore, n);

        if (p != Integer.MAX_VALUE) {
            System.out.println(p);
        } else {
            System.out.println("Não foi possível montar uma árvore a partir das arestas fornecidas.");
        }
    }

    // Adiciona as arestas do grafo
    public static void montaArestas(List<Aresta> arestas) {
        arestas.add(new Aresta(1, 2, 1));
        arestas.add(new Aresta(1, 5, 3));
        arestas.add(new Aresta(1, 7, 6));
        arestas.add(new Aresta(2, 3, 2));
        arestas.add(new Aresta(2, 4, 8));
        arestas.add(new Aresta(3, 5, 4));
        arestas.add(new Aresta(4, 6, 10));
        arestas.add(new Aresta(5, 6, 9));
        arestas.add(new Aresta(5, 7, 5));
        arestas.add(new Aresta(7, 3, 11));
    }

    // Executa o algoritmo de Kruskal
    public static int kruskal(List<Aresta> arestas, List<Aresta> arvore, int n) {

        // Ordena as arestas pelo peso
        Collections.sort(arestas);

        Dsu dsu = new Dsu(n);
        int pesoTotal = 0;

        for (Aresta a : arestas) {

            // Adiciona a aresta somente se ela não formar ciclo
            if (dsu.uni(a.origem, a.destino)) {
                arvore.add(a);
                pesoTotal += a.peso;

                // Para quando a árvore estiver completa
                if (arvore.size() == n - 1) {
                    break;
                }
            }
        }

        // Retorna o peso da árvore ou informa que não foi possível montá-la
        if (arvore.size() == n - 1) {
            return pesoTotal;
        }
        return Integer.MAX_VALUE;
    }
}

class Dsu {

    // Vetor que representa os conjuntos
    private int[] pais;

    public Dsu(int n) {
        pais = new int[n + 1];
        Arrays.fill(pais, -1);
    }

    // Encontra o representante de um conjunto
    public int find(int a) {
        if (pais[a] < 0) {
            return a;
        }

        pais[a] = find(pais[a]);
        return pais[a];
    }

    // Une dois conjuntos diferentes
    public boolean uni(int a, int b) {
        a = find(a);
        b = find(b);

        // Se já pertencem ao mesmo conjunto, forma ciclo
        if (a == b) {
            return false;
        }

        // União por tamanho
        if (pais[a] < pais[b]) {
            pais[a] += pais[b];
            pais[b] = a;
        } else {
            pais[b] += pais[a];
            pais[a] = b;
        }

        return true;
    }
}
