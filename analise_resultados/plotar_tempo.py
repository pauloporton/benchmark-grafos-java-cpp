"""
Gera um gráfico por combinação (algoritmo, caso), com o número de vértices (V)
no eixo X e o tempo médio de execução no eixo Y — uma linha para Java, outra
para C++.

Fontes de dado:
  Java: benchmark-jmh/experiments/results/resultado.json   (formato JMH)
  C++:  benchmark-cpp/resultados/resultados_*.json          (formato Google Benchmark)

Saída:
  static/tempo/<algoritmo>_<caso>.png   (20 arquivos: 4 algoritmos x 5 casos)

Uso (a partir da raiz do repositório):
    python3 analise_resultados/plotar_tempo.py
"""
import glob
import json
import os

import matplotlib.pyplot as plt

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JAVA_JSON = os.path.join(RAIZ, "benchmark-jmh", "experiments", "results", "resultado.json")
CPP_JSONS = os.path.join(RAIZ, "benchmark-cpp", "resultados", "resultados_*.json")
PASTA_SAIDA = os.path.join(RAIZ, "graficos", "tempo")

CORES = {"Java": "#4C72B0", "C++": "#DD8452"}


def ler_tempo_java(caminho):
    """
    Lê o resultado.json do JMH e devolve pontos (algoritmo, caso, tamanho) -> (tempo_us, erro_us).
    O JMH já reporta o score na unidade configurada em @OutputTimeUnit (aqui, us/op).
    """
    with open(caminho, encoding="utf-8") as f:
        dados = json.load(f)

    pontos = {}
    for item in dados:
        # "benchmark.BFSBenchmark.benchmarkBFS" -> "BFS"
        algoritmo = item["benchmark"].split(".")[-2].replace("Benchmark", "")
        caso = item["params"]["caso"]
        tamanho = int(item["params"]["tamanho"])

        unidade = item["primaryMetric"]["scoreUnit"]
        if unidade != "us/op":
            raise ValueError(f"Unidade inesperada no JMH: {unidade} (esperava us/op)")

        tempo_us = item["primaryMetric"]["score"]
        erro_us = item["primaryMetric"]["scoreError"]

        pontos[(algoritmo, caso, tamanho)] = (tempo_us, erro_us)

    return pontos


def _parse_run_name(run_name):
    """
    "Teste_BFS_melhor_10"          -> ("BFS", "melhor", 10)
    "Teste_Bellman_Ford_melhor_10" -> ("BellmanFord", "melhor", 10)
    """
    partes = run_name.split("_")
    tamanho = int(partes[-1])
    caso = partes[-2]
    algoritmo = "".join(partes[1:-2])  # junta "Bellman" + "Ford" -> "BellmanFord"
    return algoritmo, caso, tamanho


def ler_tempo_cpp(padrao_glob):
    """
    Lê todos os resultados_*.json do Google Benchmark e devolve pontos
    (algoritmo, caso, tamanho) -> (tempo_us, erro_us).

    O Google Benchmark reporta várias repetições brutas + agregados
    (mean/median/stddev/cv); usamos "mean" como valor e "stddev" como erro.
    O tempo vem em nanossegundos (real_time); convertemos para microssegundos
    para bater com a unidade usada do lado Java.
    """
    medias = {}
    desvios = {}

    for caminho in glob.glob(padrao_glob):
        with open(caminho, encoding="utf-8") as f:
            dados = json.load(f)

        for item in dados["benchmarks"]:
            if item.get("run_type") != "aggregate":
                continue

            algoritmo, caso, tamanho = _parse_run_name(item["run_name"])
            chave = (algoritmo, caso, tamanho)

            if item["time_unit"] != "ns":
                raise ValueError(f"Unidade inesperada no Google Benchmark: {item['time_unit']}")

            tempo_us = item["real_time"] / 1000.0

            if item["aggregate_name"] == "mean":
                medias[chave] = tempo_us
            elif item["aggregate_name"] == "stddev":
                desvios[chave] = tempo_us

    pontos = {}
    for chave, tempo_us in medias.items():
        pontos[chave] = (tempo_us, desvios.get(chave, 0.0))

    return pontos


def agrupar_por_algoritmo_caso(pontos_java, pontos_cpp):
    """(algoritmo, caso, tamanho) -> valor  vira  (algoritmo, caso) -> {linguagem: [(tamanho, valor, erro), ...]}"""
    agrupado = {}

    for (algoritmo, caso, tamanho), (valor, erro) in pontos_java.items():
        agrupado.setdefault((algoritmo, caso), {}).setdefault("Java", []).append((tamanho, valor, erro))

    for (algoritmo, caso, tamanho), (valor, erro) in pontos_cpp.items():
        agrupado.setdefault((algoritmo, caso), {}).setdefault("C++", []).append((tamanho, valor, erro))

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
            tempos = [p[1] for p in pontos]
            erros = [p[2] for p in pontos]

            plt.errorbar(
                tamanhos, tempos, yerr=erros,
                marker="o", capsize=4, linewidth=2,
                color=CORES[linguagem], label=linguagem,
            )

        plt.xlabel("Número de vértices (V)")
        plt.ylabel("Tempo médio (µs)")
        plt.xscale("log")
        plt.yscale("log")
        plt.title(f"{algoritmo} — caso: {caso}")
        plt.legend()
        plt.grid(True, which="both", linestyle="--", alpha=0.4)
        plt.tight_layout()

        caminho = os.path.join(pasta_saida, f"{algoritmo}_{caso}.png")
        plt.savefig(caminho, dpi=150)
        plt.close()
        print(f"Gráfico salvo em {caminho}")


if __name__ == "__main__":
    pontos_java = ler_tempo_java(JAVA_JSON)
    pontos_cpp = ler_tempo_cpp(CPP_JSONS)
    agrupado = agrupar_por_algoritmo_caso(pontos_java, pontos_cpp)
    plotar(agrupado, PASTA_SAIDA)
