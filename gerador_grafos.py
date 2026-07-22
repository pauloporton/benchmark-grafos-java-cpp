import random
import math
import os

#Geradores de grafos
def gerar_arvore_balanceada(V):
    arestas = []
    for i in range(2, V + 1):
        arestas.append((i//2, i))
    return arestas

def gerar_grafo_linear(V):
    arestas = []
    for i in range(1, V):
        arestas.append((i, i+1))
    return arestas

def gerar_floresta_fragmentada(V, num_comp, s = 1.5):
    tamanhos = []
    soma = 0
    for i in range(2, num_comp + 2):
        tamanho = max(round(V/i**s), 1)
        tamanhos.append(tamanho)
        soma += tamanho
    tamanhos[0] -= soma - V
    arestas = []
    regulacao = 0
    for t in tamanhos:
        sub_grafo = gerar_grafo_aleatorio(t, calcula_arestas(t, 40, False, True), True, True)
        sub_grafo_regulado = [(u + regulacao, v + regulacao) for u, v in sub_grafo]
        arestas += sub_grafo_regulado
        regulacao += t
    return arestas

def gerar_grafo_aleatorio(V, E, direcionado, conectado):
    arestas_usadas = set()
    arestas = []

    if conectado:
        arestas = gerar_arvore_balanceada(V)
        for a in arestas:
            arestas_usadas.add(normalizar(a[0], a[1], direcionado))
    while(len(arestas) < E):
        u = random.randint(1, V)
        v = random.randint(1, V)
        if u == v:
            continue
        aresta = normalizar(u, v, direcionado)
        if aresta not in arestas_usadas:
            arestas_usadas.add(aresta)
            arestas.append(aresta)
    return arestas

def normalizar(u, v, direcionado):
    if direcionado:
        return (u, v)
    return (min(u, v), max(u, v))

def calcula_arestas(V, nivel, eh_bellman, direcionado):
    E = 22.222 * V * nivel / 100 * math.log10(V)
    if(eh_bellman):
        E *= 0.01
    E = int(round(E))
    max_arestas = V * (V-1) if direcionado else (V * (V-1)) // 2
    E = min(E, max_arestas)
    return E

def adiciona_pesos(arestas):
    for i in range(len(arestas)):
        arestas[i] = (arestas[i][0], arestas[i][1], random.randint(-1000, 1000))
    return arestas

def gerar_grafo_matriz(V):
    lado = math.ceil(math.sqrt(V))
    arestas = []
    for i in range(1, V + 1):
        if i % lado != 0 and i < V:
            arestas.append((i, i + 1))
        if i + lado <= V:
            arestas.append((i, i + lado))
    arestas.reverse()
    return arestas

def escrever_arquivo_sem_peso(caminho, V, arestas):
    with open(caminho, 'w') as f:
        f.write(f"{V} {len(arestas)}\n")
        for u, v in arestas:
            f.write(f"{u} {v}\n")

def escrever_arquivo_com_peso(caminho, V, arestas, preservar_ordem = False):
    arestas_embaralhadas = arestas.copy()
    if not preservar_ordem:
        random.shuffle(arestas_embaralhadas)

    with open(caminho, 'w') as f:
        f.write(f"{V} {len(arestas_embaralhadas)}\n")
        for u, v, peso in arestas_embaralhadas:
            f.write(f"{u} {v} {peso}\n")
class Dsu:

    def __init__(self, n):
        self.pais = [-1] * (n + 1)

    def find(self, a):
        if self.pais[a] < 0:
            return a
        self.pais[a] = self.find(self.pais[a])
        return self.pais[a]

    def uni(self, a, b):
        a = self.find(a)
        b = self.find(b)

        if b == a:
            return False

        if(self.pais[a] < self.pais[b]):
            self.pais[a] += self.pais[b]
            self.pais[b] = a
        else:
            self.pais[b] += self.pais[a]
            self.pais[a] = b

        return True

    def conta_componentes(self):
        contador = 0
        for i in range(1, len(self.pais)):
            if self.pais[i] < 0:
                contador += 1
        return contador

#Validação dos grafos
def valida_grafo(V, arestas, esperado):
    problemas = []
    vertices_usados = set()
    for u, v, *_ in arestas:
        if u < 1 or u > V:
            problemas.append(f"Vértice {u} maior que {V}")
            continue
        if v < 1 or v > V:
            problemas.append(f"Vértice {v} maior que {V}")
            continue
        vertices_usados.add(u)
        vertices_usados.add(v)

    if "num_arestas" in esperado and len(arestas) != esperado.get("num_arestas"):
        E = esperado.get("num_arestas")
        problemas.append(f"{E} arestas esperadas, possui {len(arestas)}")

    if esperado.get("aciclico"):
        d = Dsu(V)
        for u, v, *_ in arestas:
            if not d.uni(u, v):
                problemas.append("Grafo possui ciclos")
                break

    if esperado.get("conectado"):
        d = Dsu(V)
        for u, v, *_ in arestas:
            d.uni(u, v)
        if d.conta_componentes() > 1:
            problemas.append("Grafo não é conectado")

    if esperado.get("num_componentes"):
        d = Dsu(V)
        for u, v, *_ in arestas:
            d.uni(u, v)
        if d.conta_componentes() != esperado["num_componentes"]:
            c = esperado["num_componentes"]
            problemas.append(f"{c} componentes esperados, possui {d.conta_componentes()}")

    if problemas:
        print(f"Validação falhou, {problemas}")
        return False
    return True

def gerar_nome_arquivo(algoritmo, caso, V):
    return f"grafos/{algoritmo}/{caso}/{V}.txt"

def gerar_estrutura(algoritmo, caso, V):
    if algoritmo == "DFS":
        if caso == "melhor":
            arestas = gerar_arvore_balanceada(V)
            esperado = {"num_arestas": V - 1, "conectado": True, "aciclico": True}
        elif caso == "pior":
            arestas = gerar_grafo_linear(V)
            esperado = {"num_arestas": V - 1, "conectado": True, "aciclico": True}
        elif caso == "esparso":
            arestas = gerar_grafo_aleatorio(V, calcula_arestas(V, 10, False, False), False, False)
            esperado = {"num_arestas": calcula_arestas(V, 10, False, False), "conectado": False, "aciclico": False}
        elif caso == "medio":
            arestas = gerar_grafo_aleatorio(V, calcula_arestas(V, 50, False, False), False, False)
            esperado = {"num_arestas": calcula_arestas(V, 50, False, False), "conectado": False, "aciclico": False}
        elif caso == "denso":
            arestas = gerar_grafo_aleatorio(V, calcula_arestas(V, 90, False, False), False, False)
            esperado = {"num_arestas": calcula_arestas(V, 90, False, False), "conectado": False, "aciclico": False}
    elif algoritmo == "BFS":
        if caso == "melhor":
            arestas = gerar_grafo_linear(V)
            esperado = {"num_arestas": V - 1, "conectado": True, "aciclico": True}
        elif caso == "pior":
            arestas = gerar_arvore_balanceada(V)
            esperado = {"num_arestas": V - 1, "conectado": True, "aciclico": True}
        elif caso == "esparso":
            arestas = gerar_grafo_aleatorio(V, calcula_arestas(V, 10, False, False), False, False)
            esperado = {"num_arestas": calcula_arestas(V, 10, False, False), "conectado": False, "aciclico": False}
        elif caso == "medio":
            arestas = gerar_grafo_aleatorio(V, calcula_arestas(V, 50, False, False), False, False)
            esperado = {"num_arestas": calcula_arestas(V, 50, False, False), "conectado": False, "aciclico": False}
        elif caso == "denso":
            arestas = gerar_grafo_aleatorio(V, calcula_arestas(V, 90, False, False), False, False)
            esperado = {"num_arestas": calcula_arestas(V, 90, False, False), "conectado": False, "aciclico": False}
    elif algoritmo == "Kruskal":
        if caso == "melhor":
            arestas = gerar_arvore_balanceada(V)
            arestas = adiciona_pesos(arestas)
            esperado = {"num_arestas": V - 1, "conectado": True, "aciclico": True}
        elif caso == "pior":
            arestas = gerar_floresta_fragmentada(V, V//5, 1.5)
            arestas = adiciona_pesos(arestas)
            esperado = {"num_componentes": V//5, "conectado": False, "aciclico": False}
        elif caso == "esparso":
            arestas = gerar_grafo_aleatorio(V, calcula_arestas(V, 10, False, True), True, False)
            arestas = adiciona_pesos(arestas)
            esperado = {"num_arestas": calcula_arestas(V, 10, False, True), "conectado": False, "aciclico": False}
        elif caso == "medio":
            arestas = gerar_grafo_aleatorio(V, calcula_arestas(V, 50, False, True), True, False)
            arestas = adiciona_pesos(arestas)
            esperado = {"num_arestas": calcula_arestas(V, 50, False, True), "conectado": False, "aciclico": False}
        elif caso == "denso":
            arestas = gerar_grafo_aleatorio(V, calcula_arestas(V, 90, False, True), True, False)
            arestas = adiciona_pesos(arestas)
            esperado = {"num_arestas": calcula_arestas(V, 90, False, True), "conectado": False, "aciclico": False}
    elif algoritmo == "BellmanFord":
        if caso == "melhor":
            arestas = gerar_arvore_balanceada(V)
            arestas = adiciona_pesos(arestas)
            esperado = {"num_arestas": V - 1, "conectado": True, "aciclico": True}
        elif caso == "pior":
            arestas = gerar_grafo_matriz(V)
            arestas = adiciona_pesos(arestas)
            esperado = {"conectado": True, "aciclico": False}
        elif caso == "esparso":
            arestas = gerar_grafo_aleatorio(V, calcula_arestas(V, 10, True, True), True, False)
            arestas = adiciona_pesos(arestas)
            esperado = {"num_arestas": calcula_arestas(V, 10, True, True), "conectado": False, "aciclico": False}
        elif caso == "medio":
            arestas = gerar_grafo_aleatorio(V, calcula_arestas(V, 50, True, True), True, False)
            arestas = adiciona_pesos(arestas)
            esperado = {"num_arestas": calcula_arestas(V, 50, True, True), "conectado": False, "aciclico": False}
        elif caso == "denso":
            arestas = gerar_grafo_aleatorio(V, calcula_arestas(V, 90, True, True), True, False)
            arestas = adiciona_pesos(arestas)
            esperado = {"num_arestas": calcula_arestas(V, 90, True, True), "conectado": False, "aciclico": False}
    return arestas, esperado

def gerar_todos_os_grafos(diretorio_saida, seed, escalas, CASOS_POR_ALGORITMO):
    random.seed(seed)

    for algoritmo, casos in CASOS_POR_ALGORITMO.items():
        for caso in casos:
            for V in escalas:
                caminho = gerar_nome_arquivo(algoritmo, caso, V)
                os.makedirs(os.path.dirname(caminho), exist_ok=True)

                arestas, esperado = gerar_estrutura(algoritmo, caso, V)

                if not valida_grafo(V, arestas, esperado):
                    print(f"ATENÇÃO: {caminho} não passou na validação")
                    continue

                if algoritmo in ("Kruskal", "BellmanFord"):
                    if algoritmo == "BellmanFord" and caso == "pior":
                        escrever_arquivo_com_peso(caminho, V, arestas, True)
                    else:
                        escrever_arquivo_com_peso(caminho, V, arestas)
                else:
                    escrever_arquivo_sem_peso(caminho, V, arestas)

    print("Geração completa.")

def main():
    CASOS_POR_ALGORITMO = {
    "DFS":           ["melhor", "pior", "esparso", "medio", "denso"],
    "BFS":           ["melhor", "pior", "esparso", "medio", "denso"],
    "Kruskal":       ["melhor", "pior", "esparso", "medio", "denso"],
    "BellmanFord":   ["melhor", "pior", "esparso", "medio", "denso"],
    }

    escalas_teste = [10, 30, 100]
    gerar_todos_os_grafos("grafos_teste", 42, escalas_teste, CASOS_POR_ALGORITMO)

main()

