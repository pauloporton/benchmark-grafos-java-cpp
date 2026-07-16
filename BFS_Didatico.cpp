#include <vector>
#include <iostream>
#include <queue>

void bfs(std::vector<std::vector<int>>& grafo, std::vector<int>& caminho, std::vector<bool>& usados, int origem) {
    //criação da fila de caminhamento da bfs
    std::queue<int> fila;
    //percorrendo o grafo inteiro com bfs a partir da origem para esse componente até a fila ficar vazia
    fila.push(origem);
    usados[origem] = true;
    while(!fila.empty()) {
        //pega o nó no topo da fila e depois o remove
        int atual = fila.front();
        fila.pop();
        //adiciona o nó no caminho percorrido
        caminho.push_back(atual);
        //adiciona os vizinhos do nó atual na fila caso não tenham sido visitados ainda e marca como usado
        for(int vizinho : grafo[atual]) {
            if(!usados[vizinho]) {
                fila.push(vizinho);
                usados[vizinho] = true;
            }
        }
    }
}


//teste simples de grafo bidirecional com 6 nós, caso desejado mude os valores abaixo para testar outros casos
void monta_grafo(std::vector<std::vector<int>>& grafo) {
    grafo[1].push_back(3);
    grafo[3].push_back(1);

    grafo[1].push_back(2);
    grafo[2].push_back(1);

    grafo[3].push_back(4);
    grafo[4].push_back(3);

    grafo[2].push_back(3);
    grafo[3].push_back(2);

    grafo[5].push_back(6);
    grafo[6].push_back(5);
}
    

int main() {
    //leitura do número de nós
    int n = 6;
    //criação do grafo 1-indexado com tamanho igual a número de nós + 1
    std::vector<std::vector<int>> grafo(n + 1);
    monta_grafo(grafo);
    //criação do armazenamento do caminho percorrido
    std::vector<int> caminho;
    //criação de vetor de nós usados para evitar ciclos infinitos e recurssões desnecessárias
    std::vector<bool> usados(n + 1, false);

    for(int i = 1; i <= n; i++) {
        if(!usados[i]) {
            bfs(grafo, caminho, usados, i);
        }
    }

    //imprimindo o caminho realizado
    for(int no : caminho) {
        std::cout << no << ' ';
    }
    return 0;
}

