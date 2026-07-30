"""
Converte o resultado bruto do JMH (JSON) para um formato normalizado (CSV),
comum entre Java e C++, que o plot_resultados.py consegue ler dos dois lados.

Colunas do CSV normalizado:
    linguagem,algoritmo,caso,tamanho,tempo_medio,erro,unidade

Uso:
    python normalizar_java.py experiments/results/resultado.json
"""
import csv
import json
import os
import sys

SAIDA_PADRAO = "experiments/results/resultados_normalizados.csv"


def normalizar(caminho_json):
    with open(caminho_json, encoding="utf-8") as f:
        dados = json.load(f)

    linhas = []
    for item in dados:
        # "benchmark.BFSBenchmark.benchmarkBFS" -> "BFS"
        algoritmo = item["benchmark"].split(".")[-2].replace("Benchmark", "")
        params = item.get("params", {})
        caso = params.get("caso", "-")
        tamanho = params.get("tamanho", "-")
        score = item["primaryMetric"]["score"]
        erro = item["primaryMetric"].get("scoreError", 0)
        unidade = item["primaryMetric"]["scoreUnit"]

        linhas.append({
            "linguagem": "Java",
            "algoritmo": algoritmo,
            "caso": caso,
            "tamanho": tamanho,
            "tempo_medio": score,
            "erro": erro,
            "unidade": unidade,
        })

    return linhas


def salvar(linhas, caminho_saida):
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)

    # Se já existir um CSV normalizado (por exemplo, com resultados do C++
    # adicionados por outro script), remove só as linhas antigas de "Java"
    # antes de escrever as novas — preserva o que não é Java.
    existentes = []
    if os.path.exists(caminho_saida):
        with open(caminho_saida, newline="", encoding="utf-8") as f:
            existentes = [linha for linha in csv.DictReader(f) if linha["linguagem"] != "Java"]

    todas = existentes + linhas

    with open(caminho_saida, "w", newline="", encoding="utf-8") as f:
        campos = ["linguagem", "algoritmo", "caso", "tamanho", "tempo_medio", "erro", "unidade"]
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(todas)

    print(f"{len(linhas)} resultados de Java normalizados em {caminho_saida}")


if __name__ == "__main__":
    caminho_json = sys.argv[1] if len(sys.argv) > 1 else "experiments/results/resultado.json"
    caminho_saida = sys.argv[2] if len(sys.argv) > 2 else SAIDA_PADRAO

    linhas = normalizar(caminho_json)
    salvar(linhas, caminho_saida)