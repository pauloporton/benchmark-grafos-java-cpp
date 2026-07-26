"""
Lê o resultado.json gerado pelo JMH e gera um gráfico separado para cada
combinação (algoritmo, caso), com o tamanho do grafo (V) no eixo X e o
tempo médio no eixo Y.

Uso:
    python plot_resultados.py resultado.json
    python plot_resultados.py resultado.json --saida graficos/
"""
import json
import os
import sys
import matplotlib.pyplot as plt


def carregar(caminho_json):
    with open(caminho_json, encoding="utf-8") as f:
        return json.load(f)


def extrair_series(dados):
    """
    Agrupa os resultados por (algoritmo, caso), cada grupo virando uma série
    de pontos (tamanho, tempo_medio, erro), ordenada por tamanho crescente.

    Cada item de "dados" tem o formato:
      benchmark: "benchmark.BFSBenchmark.benchmarkBFS"
      params: {"caso": "denso", "tamanho": "100"}
      primaryMetric.score: tempo médio
      primaryMetric.scoreError: margem de erro (desvio)
      primaryMetric.scoreUnit: unidade (ex: "us/op")
    """
    series = {}  # (algoritmo, caso) -> lista de (tamanho, score, erro, unidade)

    for item in dados:
        algoritmo = item["benchmark"].split(".")[-2]  # ex: BFSBenchmark
        params = item.get("params", {})
        caso = params.get("caso", "-")
        tamanho = int(params.get("tamanho", 0))
        score = item["primaryMetric"]["score"]
        erro = item["primaryMetric"].get("scoreError", 0)
        unidade = item["primaryMetric"]["scoreUnit"]

        chave = (algoritmo, caso)
        series.setdefault(chave, []).append((tamanho, score, erro, unidade))

    for chave in series:
        series[chave].sort(key=lambda ponto: ponto[0])  # ordena por tamanho

    return series


def plotar_series(series, pasta_saida="graficos"):
    os.makedirs(pasta_saida, exist_ok=True)

    for (algoritmo, caso), pontos in series.items():
        tamanhos = [p[0] for p in pontos]
        tempos = [p[1] for p in pontos]
        erros = [p[2] for p in pontos]
        unidade = pontos[0][3]

        plt.figure(figsize=(6, 4.5))
        plt.errorbar(
            tamanhos, tempos, yerr=erros,
            marker="o", capsize=4, color="#4C72B0", linewidth=2
        )
        plt.xlabel("Tamanho do grafo (V)")
        plt.ylabel(f"Tempo médio ({unidade})")
        plt.title(f"{algoritmo} — caso: {caso}")
        plt.xticks(tamanhos)  # só marca os tamanhos que existem (10, 30, 100...)
        plt.grid(True, linestyle="--", alpha=0.4)
        plt.tight_layout()

        nome_arquivo = f"{algoritmo}_{caso}.png"
        caminho = os.path.join(pasta_saida, nome_arquivo)
        plt.savefig(caminho, dpi=150)
        plt.close()

        print(f"Gráfico salvo em {caminho}")


if __name__ == "__main__":
    argumentos = sys.argv[1:]
    caminho_json = argumentos[0] if argumentos and not argumentos[0].startswith("--") else "resultado.json"

    pasta_saida = "graficos"
    if "--saida" in argumentos:
        pasta_saida = argumentos[argumentos.index("--saida") + 1]

    dados = carregar(caminho_json)
    series = extrair_series(dados)
    plotar_series(series, pasta_saida)