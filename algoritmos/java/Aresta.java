package algoritmos.java;

public class Aresta implements Comparable<Aresta>{
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