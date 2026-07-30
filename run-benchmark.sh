#!/bin/bash
set -e

echo "Gerando grafos..."
python3 gerador_grafos.py

echo "Compilando projeto Java..."
cd benchmark-jmh
mvn clean package

echo "Executando benchmarks Java..."
mkdir -p experiments/results
java -jar target/benchmarks.jar \
  -rf json \
  -rff experiments/results/resultado.json

echo "Medindo pico de memória (RSS) de cada combinação..."
if [ -f "medir_memoria.sh" ]; then
    chmod +x medir_memoria.sh
    ./medir_memoria.sh
else
    echo "Aviso: medir_memoria.sh não encontrado em benchmark-jmh/, pulando essa etapa."
fi

cd ..   # <-- volta para a raiz do projeto antes de entrar no C++

echo "Compilando benchmarks C++..."
cd benchmark-cpp
g++ -O2 -std=c++17 benchmark_bfs.cpp -o BFS_benchmark -lbenchmark -lpthread
g++ -O2 -std=c++17 benchmark_dfs.cpp -o DFS_benchmark -lbenchmark -lpthread
g++ -O2 -std=c++17 benchmark_kruskal.cpp -o Kruskal_benchmark -lbenchmark -lpthread
g++ -O2 -std=c++17 benchmark_bellmanford.cpp -o BellmanFord_benchmark -lbenchmark -lpthread

mkdir -p resultados

echo "Rodando BFS (C++)..."
./BFS_benchmark --benchmark_repetitions=20 --benchmark_format=json --benchmark_out=resultados/resultados_bfs.json

echo "Rodando DFS (C++)..."
./DFS_benchmark --benchmark_repetitions=20 --benchmark_format=json --benchmark_out=resultados/resultados_dfs.json

echo "Rodando Kruskal (C++)..."
./Kruskal_benchmark --benchmark_repetitions=20 --benchmark_format=json --benchmark_out=resultados/resultados_kruskal.json

echo "Rodando Bellman-Ford (C++)..."
./BellmanFord_benchmark --benchmark_repetitions=20 --benchmark_format=json --benchmark_out=resultados/resultados_bellmanford.json

cd ..   # volta pra raiz de novo, antes das próximas etapas

echo "Gerando gráficos..."
if [ -d "venv" ]; then
    source venv/bin/activate
fi
python3 normalizar_java.py benchmark-jmh/experiments/results/resultado.json
python3 plot_resultados.py --saida static/

echo "Processo finalizado com sucesso."
