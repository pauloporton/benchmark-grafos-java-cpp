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

<<<<<<< HEAD
echo "Medindo pico de memória (RSS) de cada combinação..."
=======
echo "Medindo pico de mem├│ria (RSS) de cada combina├º├úo..."
>>>>>>> 8b72fb6c033f7be0fc0d2fcd81618a965e10bce6
if [ -f "medir_memoria.sh" ]; then
    chmod +x medir_memoria.sh
    ./medir_memoria.sh
else
<<<<<<< HEAD
    echo "Aviso: medir_memoria.sh não encontrado em benchmark-jmh/, pulando essa etapa."
=======
    echo "Aviso: medir_memoria.sh n├úo encontrado em benchmark-jmh/, pulando essa etapa."
>>>>>>> 8b72fb6c033f7be0fc0d2fcd81618a965e10bce6
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

echo "Medindo memoria (C++)..."
chmod +x ./medir_memoria_cpp.sh
./medir_memoria_cpp.sh

<<<<<<< HEAD
cd ..   # volta pra raiz de novo, antes das próximas etapas

echo "Gerando gráficos..."
=======
cd ..   # volta pra raiz de novo, antes das pr├│ximas etapas

echo "Gerando gráficos..."
>>>>>>> 8b72fb6c033f7be0fc0d2fcd81618a965e10bce6
if [ -d "venv" ]; then
    source venv/bin/activate
fi
python3 normalizar_java.py benchmark-jmh/experiments/results/resultado.json
python3 plot_resultados.py --saida static/

echo "Processo finalizado com sucesso."
