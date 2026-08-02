"""
Lê o CSV normalizado (experiments/results/resultados_normalizados.csv) e gera
um gráfico separado para cada combinação (algoritmo, caso), com o tamanho do
grafo (V) no eixo X e o tempo médio no eixo Y — uma linha por linguagem
presente no CSV (Java e/ou C++).

Uso:
    python plot_resultados.py
    python plot_resultados.py experiments/results/resultados_normalizados.csv --saida static/
"""
import csv
import os
import sys
import matplotlib.pyplot as plt

CORES_POR_LINGUAGEM = {
    "Java": "#4C72B0",
    "C++": "#DD8452",
}


def carregar(caminho_csv):
    with open(caminho_csv, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def extrair_series(linhas):
    """
    Agrupa os resultados por (algoritmo, caso, linguagem), cada grupo virando
    uma série de pontos (tamanho, tempo_medio, erro), ordenada por tamanho.
    """
    series = {}  # (algoritmo, caso, linguagem) -> lista de (tamanho, tempo, erro, unidade)

    for linha in linhas:
        chave = (linha["algoritmo"], linha["caso"], linha["linguagem"])
        ponto = (
            int(linha["tamanho"]),
            float(linha["tempo_medio"]),
            float(linha["erro"]),
            linha["unidade"],
        )
        series.setdefault(chave, []).append(ponto)

    for chave in series:
        series[chave].sort(key=lambda ponto: ponto[0])

    return series


def agrupar_por_algoritmo_caso(series):
    """Reagrupa (algoritmo, caso, linguagem) -> pontos em (algoritmo, caso) -> {linguagem: pontos}."""
    agrupado = {}
    for (algoritmo, caso, linguagem), pontos in series.items():
        agrupado.setdefault((algoritmo, caso), {})[linguagem] = pontos
    return agrupado


def plotar(agrupado, pasta_saida="static"):
    os.makedirs(pasta_saida, exist_ok=True)

    for (algoritmo, caso), por_linguagem in agrupado.items():
        plt.figure(figsize=(6, 4.5))

        unidade = "?"
        for linguagem, pontos in sorted(por_linguagem.items()):
            tamanhos = [p[0] for p in pontos]
            tempos = [p[1] for p in pontos]
            erros = [p[2] for p in pontos]
            unidade = pontos[0][3]

            cor = CORES_POR_LINGUAGEM.get(linguagem, "#55A868")
            plt.errorbar(
                tamanhos, tempos, yerr=erros,
                marker="o", capsize=4, color=cor, linewidth=2,
                label=linguagem,
            )

        plt.xlabel("Tamanho do grafo (V)")
        plt.ylabel(f"Tempo médio ({unidade})")
        plt.title(f"{algoritmo} — caso: {caso}")
        plt.legend()
        plt.grid(True, linestyle="--", alpha=0.4)
        plt.tight_layout()

        nome_arquivo = f"{algoritmo}_{caso}.png"
        caminho = os.path.join(pasta_saida, nome_arquivo)
        plt.savefig(caminho, dpi=150)
        plt.close()

        print(f"Gráfico salvo em {caminho}")


if __name__ == "__main__":
    argumentos = sys.argv[1:]
    caminho_csv = argumentos[0] if argumentos and not argumentos[0].startswith("--") else "experiments/results/resultados_normalizados.csv"

    pasta_saida = "static"
    if "--saida" in argumentos:
        pasta_saida = argumentos[argumentos.index("--saida") + 1]

    linhas = carregar(caminho_csv)
    series = extrair_series(linhas)
    agrupado = agrupar_por_algoritmo_caso(series)
    plotar(agrupado, pasta_saida)