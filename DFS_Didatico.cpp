#include <vector>
#include <iostream>

void dfs(std::vector<std::vector<int>>& grafo, std::vector<int>& caminho, std::vector<bool>& usados, int no) {
    //visita o nó na lista de usados
    usados[no] = true;
    //adiciona o nó no caminho percorrido
    caminho.push_back(no);
    //caminha em profundidade nos vizinhos
    for(int vizinho : grafo[no]) {
        //checa se o vizinho já foi visitado para evitar ciclos infinitos
        if(!usados[vizinho]) {
            dfs(grafo, caminho, usados, vizinho);
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
    //percorrendo o grafo inteiro com dfs a partir do nó 1
    for(int i = 1; i <= n; i++) {
        //verificando se o nó já foi usado
        if(!usados[i]) {
            dfs(grafo, caminho, usados, i);
        }
    }

    //imprimindo o caminho realizado
    for(int no : caminho) {
        std::cout << no << ' ';
    }
    return 0;
}

