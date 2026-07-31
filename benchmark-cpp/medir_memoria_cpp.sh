#!/bin/bash
set -e

ALGORITMOS=("BFS" "DFS" "Kruskal" "BellmanFord")
CASOS=("melhor" "pior" "esparso" "medio" "denso")
ESCALAS=(10 30 100 300 1000 3000 10000 30000 100000)

SAIDA="resultados/memoria_cpp.csv"
mkdir -p resultados
echo "algoritmo,caso,escala,memoria_kb" > "$SAIDA"

for algoritmo in "${ALGORITMOS[@]}"; do
    binario="./${algoritmo}_benchmark"

    if [ ! -f "$binario" ]; then
        echo "Aviso: $binario nao encontrado, pulando."
        continue
    fi

    for caso in "${CASOS[@]}"; do
        for escala in "${ESCALAS[@]}"; do
            nome_filtro="${caso}_${escala}$"

            # Roda 1 vez, sem repeticoes (soh precisamos do pico de memoria)
            log_tmp=$(mktemp)
            /usr/bin/time -v "$binario" --benchmark_filter="$nome_filtro" > /dev/null 2> "$log_tmp"

            memoria=$(grep "Maximum resident set size" "$log_tmp" | awk '{print $NF}')

            if [ -z "$memoria" ]; then
                echo "Aviso: nao foi possivel medir memoria para $algoritmo $caso $escala"
                memoria="NA"
            fi

            echo "$algoritmo,$caso,$escala,$memoria" >> "$SAIDA"
            rm -f "$log_tmp"
        done
    done
done

echo "Medicao de memoria concluida. Resultados em $SAIDA"
