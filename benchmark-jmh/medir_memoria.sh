#!/bin/bash
# Roda cada combinação de benchmark/caso/tamanho isoladamente, medindo o
# pico de memória (RSS) do processo Java via /usr/bin/time -v.
#
# Uso: ./medir_memoria.sh
# Saída: experiments/results/memoria_resultados.csv

set -e

JAR="target/benchmarks.jar"
SAIDA_CSV="experiments/results/memoria_resultados.csv"

mkdir -p experiments/results

BENCHMARKS=("BFSBenchmark" "DFSBenchmark" "KruskalBenchmark" "BellmanFordBenchmark")
CASOS=("melhor" "pior" "esparso" "medio" "denso")
TAMANHOS=("10" "30" "100" "300" "1000" "3000" "10000" "30000" "100000")

echo "benchmark,caso,tamanho,pico_memoria_kb" > "$SAIDA_CSV"

for bench in "${BENCHMARKS[@]}"; do
  for caso in "${CASOS[@]}"; do
    for tamanho in "${TAMANHOS[@]}"; do
      echo ">> Medindo $bench / $caso / $tamanho"

      log_tmp=$(mktemp)

      # -f 1: um fork (já é o padrão, mas deixa explícito)
      # -wi/-i baixos aqui só para não gastar tempo demais medindo memória;
      # ajuste se quiser warmup/iterações completos também na medição de memória
      /usr/bin/time -v java -Xms64m -Xmx512m -jar "$JAR" "$bench" \
        -p caso="$caso" -p tamanho="$tamanho" \
        -f 1 -wi 1 -i 1 \
        > /dev/null 2> "$log_tmp"

      pico_kb=$(grep "Maximum resident set size" "$log_tmp" | awk -F': ' '{print $2}')

      echo "$bench,$caso,$tamanho,$pico_kb" >> "$SAIDA_CSV"

      rm "$log_tmp"
    done
  done
done

echo "Concluído. Resultados em $SAIDA_CSV"
