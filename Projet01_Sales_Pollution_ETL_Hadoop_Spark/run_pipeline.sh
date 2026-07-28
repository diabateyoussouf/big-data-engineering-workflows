#!/usr/bin/env bash

# Arrêter le script en cas d'erreur
set -e

echo "=================================================="
echo "🚀 DÉMARRAGE DU PIPELINE BIG DATA END-TO-END"
echo "=================================================="

# 1. Vérification du dossier data
if [ ! -f "data/purchases.txt" ] || [ ! -f "data/AirPollution.txt" ]; then
    echo "❌ Erreur : Les fichiers bruts sont manquants dans data/"
    exit 1
fi

# 2. Exécution des tests MapReduce (Legacy Layer)
echo ""
echo "--- [1/3] 🐘 Exécution des traitements Hadoop MapReduce ---"
cat data/purchases.txt | python3 mapreduce/mapper_sales.py | sort | python3 mapreduce/reducer_sales.py > data/mr_sales_output.txt
echo "✅ MapReduce Sales terminé. Extrait des résultats :"
head -n 5 data/mr_sales_output.txt

cat data/AirPollution.txt | python3 mapreduce/mapper_pollution.py | sort | python3 mapreduce/reducer_pollution.py > data/mr_pollution_output.txt
echo "✅ MapReduce Pollution terminé. Extrait des résultats :"
head -n 5 data/mr_pollution_output.txt

# 3. Exécution des pipelines PySpark (Modern Layer & Parquet Generation)
echo ""
echo "--- [2/3] ⚡ Exécution des traitements PySpark ETL ---"
python3 pyspark/sales_etl.py
python3 pyspark/pollution_etl.py

# 4. Lancement de la couche Serving & Dashboard
echo ""
echo "--- [3/3] 📊 Lancement du Dashboard Streamlit ---"
echo "URL : http://localhost:8501"
streamlit run dashboard/app.py