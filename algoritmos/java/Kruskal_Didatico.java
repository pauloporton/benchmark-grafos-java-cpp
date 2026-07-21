package algoritmos.java;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

public class Kruskal_Didatico {
    public static void main(String[] args) {
        int n = 7;

        List<Aresta> arestas = new ArrayList<>();
        montaArestas(arestas);

        List<Aresta> arvore = new ArrayList<>();
        int p = kruskal(arestas, arvore, n);

        if (p != Integer.MAX_VALUE) {
            System.out.println(p);
        } else {
            System.out.println("Não foi possível montar uma árvore a partir das arestas fornecidas.");
        }
    }

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

    public static int kruskal(List<Aresta> arestas, List<Aresta> arvore, int n) {
        Collections.sort(arestas);

        Dsu dsu = new Dsu(n);
        int pesoTotal = 0;

        for (Aresta a : arestas) {
            if (dsu.uni(a.origem, a.destino)) {
                arvore.add(a);
                pesoTotal += a.peso;
                if (arvore.size() == n-1) {
                    break;
                }
            }
        }

        if (arvore.size() == n-1) {
            return pesoTotal;
        }
        return Integer.MAX_VALUE;
    }
}

class Dsu {
    private int[] pais;

    public Dsu(int n) {
        pais = new int[n+1];
        Arrays.fill(pais, -1);
    }

    public int find(int a) {
        if (pais[a] < 0) {
            return a;
        }

        pais[a] = find(pais[a]);
        return pais[a];
    }

    public boolean uni(int a, int b) {
        a = find(a);
        b = find(b);

        if (a == b)  {
            return false;
        }

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

class Aresta implements Comparable<Aresta>{
    int origem;
    int destino;
    int peso;

    public Aresta(int u, int v, int p) {
        this.origem = u;
        this.destino = v;
        this.peso = p;
    }

    @Override
    public int compareTo(Aresta outra) {
        return Integer.compare(this.peso, outra.peso);
    }
}
