# 📊 Big Data Engineering Workflows & Business Analytics

[![Live Dashboard](https://img.shields.io/badge/Streamlit_Cloud-Live_App-red?style=for-the-badge&logo=streamlit)](https://hadoop-pyspark-dashboard.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![PySpark](https://img.shields.io/badge/PySpark-4.2.0-orange?style=for-the-badge&logo=apachespark)](https://spark.apache.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

<!-- 🎨 EMPLACEMENT IMAGE IA 1 : BANNIÈRE PRINCIPALE -->
<!-- PROMPT IA RECOMMANDE (Midjourney / DALL-E) :
"A futuristic dark-mode data engineering pipeline dashboard banner, showing Spark data streams flowing into interactive charts, high-tech isometric style, blue and purple glowing lines, clean 8k render" -->
<p align="center">
  <img width="2172" height="724" alt="image" src="https://github.com/user-attachments/assets/774e3b6c-b2fd-492a-a01f-d24151507d74" />
</p>

## 📌 Présentation du Projet

Ce dépôt centralise une suite de **workflows d'ingénierie Big Data et de tableaux de bord décisionnels**. Son objectif est de démontrer la transformation de volumes importants de données brutes en **indicateurs métiers à haute valeur ajoutée** grâce à des architectures distribuées modernes.

Le cas d'usage principal (**`Projet01`**) couvre le secteur du **Retail / E-commerce** ainsi que la **Télémétrie Environnementale**, tout en illustrant le gain de performance apporté par la migration d'une architecture Hadoop MapReduce vers une architecture in-memory avec **PySpark**.

🔗 **Accès direct au Dashboard en ligne :** [hadoop-pyspark-dashboard.streamlit.app](https://hadoop-pyspark-dashboard.streamlit.app/)

---

## 🛠️ Stack Technique & Écosystème

| Catégorie | Technologies Utilisées |
| :--- | :--- |
| **Ingestion & Traitement** | `PySpark 4.2.0`, `Hadoop MapReduce`, `Python 3.10+` |
| **Stockage Optimisé** | `Apache Parquet` (Format colonne compressé) |
| **Visualisation & Dashboard** | `Streamlit 1.60`, `Plotly Express`, `Pandas` |
| **Déploiement & Cloud** | `Streamlit Cloud`, `Git / GitHub` |
| **Environnement** | `Linux (Ubuntu)`, `Virtualenv` |

---

## 🏗️ Architecture & Pipeline de Données

<!-- 🎨 EMPLACEMENT IMAGE IA 2 : SCHÉMA D'ARCHITECTURE -->
<!-- PROMPT IA RECOMMANDE :
"An elegant dark mode architectural diagram of a Big Data Pipeline: Raw TXT/CSV Files -> Apache Spark Processing -> Aggregated Parquet Files -> Streamlit Cloud Dashboard, modern vector icon style" -->
<p align="center">
  <img width="1672" height="941" alt="image" src="https://github.com/user-attachments/assets/8e0da92a-9b1c-4950-b3a0-ab82f206f517" />

</p>

1. **Extraction & Nettoyage :** Ingestion des fichiers bruts de ventes (`purchases.txt`) et des métriques de pollution urbaine.
2. **ETL Distribué (PySpark) :** Nettoyage, agrégations à grande échelle et calcul des KPIs financiers et environnementaux.
3. **Stockage Optimisé :** Persistence des résultats agrégés sous forme de fichiers **Parquet** légers.
4. **Restitution Décisionnelle :** Visualisation interactive déployée sur **Streamlit Cloud**.

---

## 🚀 Fonctionnalités du Dashboard

<!-- 🎨 EMPLACEMENT IMAGE IA 3 : MOCKUP DASHBOARD -->
<!-- PROMPT IA RECOMMANDE :
"A sleek laptop device mockup displaying a modern business analytics dashboard with bar charts, pie charts and scatter plots, dark aesthetic, clean interface" -->
<p align="center">
  <img width="1672" height="941" alt="image" src="https://github.com/user-attachments/assets/6a797c40-41d8-4b12-b5ca-9bb2aa7cf40e" />

</p>

* 🛒 **Performance Commerciale :** Analyse du Chiffre d'Affaires global, répartition hebdomadaire des ventes et Top 10 des catégories produits.
* 🌍 **Surveillance Environnementale :** Étude de corrélation entre température et concentrations de pollutions ($O_3$, $CO$).
* 💡 **Benchmark d'Architecture :** Comparatif d'impact ROI et de performance entre Hadoop et PySpark.

---

## 📂 Structure du Dépôt

```text
big-data-engineering-workflows/
├── requirements.txt                   # Dépendances du déploiement Cloud
├── .gitignore                         # Exclusions Git (fichiers bruts > 100 Mo, caches)
├── README.md                          # Documentation principale
│
└── Projet01_Sales_Pollution_ETL_Hadoop_Spark/
    ├── dashboard/
    │   └── app.py                     # Code de l'application Streamlit
    ├── data/                          # Fichiers Parquet agrégés issus de l'ETL
    │   ├── processed_sales_by_day.parquet
    │   ├── processed_sales_by_category.parquet
    │   ├── processed_sales_by_store.parquet
    │   ├── processed_pollution_full.parquet
    │   └── processed_co_monthly.parquet
    ├── run_pipeline.sh                # Script d'exécution de l'ETL local
    └── README.md                      # Documentation spécifique au Projet 01
