package benchmark;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import algoritmos.java.Aresta;

/*
 Lê os arquivos de grafo gerados pelo gerador_grafos.py
 Formato dos arquivos:
 1ª linha:  "(nº de vertices) (nº de arestas)"
 2ª linha e seguintes: "(origem) (destino)"           sem peso: (BFS e DFS) ou
                       "(origem) (destino) (peso)"    com peso: (Kruskal e BellmanFord)
 */
public class LeitorGrafo {
    
    // lê grafo sem peso e retorna lista de adjacencia (BFS e DFS)
    public static List<List<Integer>> lerListaAdjacencia(String caminho) {
        List<List<Integer>> adjacencia = new ArrayList<>();

        // tentativa de abertura do arquivo descrito no caminho
        try (BufferedReader br = new BufferedReader(new FileReader(caminho))) {

            // pega o numero de vertices e numero de arestas do grafo
            String[] cabecalho =  br.readLine().split(" ");
            int v = Integer.parseInt(cabecalho[0]);
            int e = Integer.parseInt(cabecalho[1]);

            // cria a lista de adjacencia
            for (int i = 0; i <= v; i++) {
                adjacencia.add(new ArrayList<>());
            }

            // preenche a lista de adjacencia para que cada lista guarde todos os vizinhos do seu vértice
            for (int i = 0; i < e; i++) {
                String[] partes = br.readLine().split(" ");
                int u = Integer.parseInt(partes[0]);
                int w = Integer.parseInt(partes[1]);

                adjacencia.get(u).add(w);
                adjacencia.get(w).add(u);
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
 
        return adjacencia;
    }

    // lê grafos com pesos e retorna lista de arestas (Kruskal e BellmanFord)
    public static List<Aresta> lerArestas(String caminho) {
        List<Aresta> arestas = new ArrayList<>();

        // tentativa de abertura do arquivo descrito no caminho
        try (BufferedReader br = new BufferedReader(new FileReader(caminho))) {

            // pega o número de arestas do grafo
            String[] cabecalho = br.readLine().split(" ");
            int e = Integer.parseInt(cabecalho[1]);

            // preenche a lista de arestas para que cada aresta tenha as informações de origem, destino e peso
            for (int i = 0; i < e; i++) {
                String[] partes = br.readLine().split(" ");
                int u = Integer.parseInt(partes[0]);
                int v = Integer.parseInt(partes[1]);
                int peso = Integer.parseInt(partes[2])

                arestas.add(new Aresta(u, v, peso));
            }

        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        
        return arestas;

    }

    // retorna o numero de vertices do grafos (usado para Kruskal e BellmanFord)
    public static int lerNumeroVertices(String caminho) {

        // tentativa de abertura do arquivo descrito no caminho
        try (BufferedReader br = new BufferedReader(new FileReader(caminho))) {

            // pega o numero de vertices do grafo e retorna
            String[] cabecalho = br.readLine().split(" ");
            return Integer.parseInt(cabecalho[0]);

        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
