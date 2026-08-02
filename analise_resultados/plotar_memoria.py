"""
Gera um gráfico por combinação (algoritmo, caso), com o número de vértices (V)
no eixo X e o pico de memória (KB) no eixo Y — uma linha para Java, outra
para C++.

Fontes de dado:
  Java: benchmark-jmh/experiments/results/memoria_resultados.csv
        colunas: benchmark,caso,tamanho,pico_memoria_kb
  C++:  benchmark-cpp/resultados/memoria_cpp.csv
        colunas: algoritmo,caso,escala,memoria_kb

Saída:
  static/memoria/<algoritmo>_<caso>.png   (20 arquivos: 4 algoritmos x 5 casos)

Uso (a partir da raiz do repositório):
    python3 analise_resultados/plotar_memoria.py
"""
import csv
import os

import matplotlib.pyplot as plt

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JAVA_CSV = os.path.join(RAIZ, "benchmark-jmh", "experiments", "results", "memoria_resultados.csv")
CPP_CSV = os.path.join(RAIZ, "benchmark-cpp", "resultados", "memoria_cpp.csv")
PASTA_SAIDA = os.path.join(RAIZ, "static", "memoria")

CORES = {"Java": "#4C72B0", "C++": "#DD8452"}


def ler_memoria_java(caminho):
    """benchmark,caso,tamanho,pico_memoria_kb -> (algoritmo, caso, tamanho) -> memoria_kb"""
    pontos = {}
    with open(caminho, newline="", encoding="utf-8") as f:
        for linha in csv.DictReader(f):
            algoritmo = linha["benchmark"].replace("Benchmark", "")
            caso = linha["caso"]
            tamanho = int(linha["tamanho"])
            pontos[(algoritmo, caso, tamanho)] = float(linha["pico_memoria_kb"])
    return pontos


def ler_memoria_cpp(caminho):
    """algoritmo,caso,escala,memoria_kb -> (algoritmo, caso, tamanho) -> memoria_kb"""
    pontos = {}
    with open(caminho, newline="", encoding="utf-8") as f:
        for linha in csv.DictReader(f):
            algoritmo = linha["algoritmo"]
            caso = linha["caso"]
            tamanho = int(linha["escala"])
            pontos[(algoritmo, caso, tamanho)] = float(linha["memoria_kb"])
    return pontos


def agrupar_por_algoritmo_caso(pontos_java, pontos_cpp):
    agrupado = {}

    for (algoritmo, caso, tamanho), valor in pontos_java.items():
        agrupado.setdefault((algoritmo, caso), {}).setdefault("Java", []).append((tamanho, valor))

    for (algoritmo, caso, tamanho), valor in pontos_cpp.items():
        agrupado.setdefault((algoritmo, caso), {}).setdefault("C++", []).append((tamanho, valor))

    for chave in agrupado:
        for linguagem in agrupado[chave]:
            agrupado[chave][linguagem].sort(key=lambda p: p[0])

    return agrupado


def plotar(agrupado, pasta_saida):
    os.makedirs(pasta_saida, exist_ok=True)

    for (algoritmo, caso), por_linguagem in sorted(agrupado.items()):
        plt.figure(figsize=(6, 4.5))

        for linguagem in ("Java", "C++"):
            if linguagem not in por_linguagem:
                continue
            pontos = por_linguagem[linguagem]
            tamanhos = [p[0] for p in pontos]
            memorias = [p[1] for p in pontos]

            plt.plot(
                tamanhos, memorias,
                marker="o", linewidth=2,
                color=CORES[linguagem], label=linguagem,
            )

        plt.xlabel("Número de vértices (V)")
        plt.ylabel("Pico de memória (KB)")
        plt.xscale("log")
        plt.title(f"{algoritmo} — caso: {caso}")
        plt.legend()
        plt.grid(True, which="both", linestyle="--", alpha=0.4)
        plt.tight_layout()

        caminho = os.path.join(pasta_saida, f"{algoritmo}_{caso}.png")
        plt.savefig(caminho, dpi=150)
        plt.close()
        print(f"Gráfico salvo em {caminho}")


if __name__ == "__main__":
    pontos_java = ler_memoria_java(JAVA_CSV)
    pontos_cpp = ler_memoria_cpp(CPP_CSV)
    agrupado = agrupar_por_algoritmo_caso(pontos_java, pontos_cpp)
    plotar(agrupado, PASTA_SAIDA)