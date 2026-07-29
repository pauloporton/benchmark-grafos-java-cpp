#!/bin/bash
# Roda o experimento completo: gera os grafos, compila o projeto Java,
# executa os benchmarks JMH e gera os gráficos de tempo por algoritmo/caso.
#
# Uso: ./run-benchmark.sh

set -e # interrompe caso tenha erro

echo "Gerando grafos..."
python3 gerador_grafos.py

echo "Compilando projeto..."
cd benchmark-jmh
mvn clean package

echo "Executando benchmarks..."
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

echo "Gerando gráficos..."
if [ -d "venv" ]; then
  source venv/bin/activate
fi
python3 normalizar_java.py experiments/results/resultado.json
python3 plot_resultados.py --saida static/

echo "Processo finalizado com sucesso."
echo "Resultados de tempo (Java) em benchmark-jmh/experiments/results/resultado.json"
echo "Resultados normalizados (Java + C++, se presente) em benchmark-jmh/experiments/results/resultados_normalizados.csv"
echo "Resultados de memória em benchmark-jmh/experiments/results/memoria_resultados.csv"
echo "Gráficos em benchmark-jmh/static/"