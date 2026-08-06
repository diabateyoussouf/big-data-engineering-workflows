# 📊 Big Data Engineering Workflows & Business Analytics

[![PySpark Dashboard](https://img.shields.io/badge/Streamlit_Cloud-Projet_01_Live-red?style=for-the-badge&logo=streamlit)](https://hadoop-pyspark-dashboard.streamlit.app/)
[![HiveQL Dashboard](https://img.shields.io/badge/Streamlit_Cloud-Projet_03_Live-orange?style=for-the-badge&logo=streamlit)](https://big-data-engineering-workflows-wvurgwswqhwdaraapmxk4a.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![PySpark](https://img.shields.io/badge/PySpark-4.2.0-orange?style=for-the-badge&logo=apachespark)](https://spark.apache.org/)
[![Apache Hive](https://img.shields.io/badge/Apache_Hive-3.1-yellow?style=for-the-badge&logo=apachehive)](https://hive.apache.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

<p align="center">
  <img width="2172" height="724" alt="Big Data Engineering Banner" src="https://github.com/user-attachments/assets/774e3b6c-b2fd-492a-a01f-d24151507d74" />
</p>

## 📌 Vision & Présentation Globale

Ce dépôt est une suite centralisée de **workflows d'ingénierie Big Data, de Feature Stores NoSQL et de tableaux de bord décisionnels propulsés par l'IA Agentique**. Il regroupe plusieurs cas d'usage industriels visant à démontrer la transformation de volumes importants de données brutes en **indicateurs métiers à haute valeur ajoutée** grâce à des architectures distribuées modernes (Hadoop, Apache Pig, Apache Hive, PySpark, Apache HBase, LangGraph, Streamlit Cloud).

Chaque sous-dossier du dépôt constitue un **projet autonome** disposant de son propre pipeline d'ETL, de son modèle de données et de sa documentation spécifique.

---

## 📚 Catalogue des Projets

| Projet | Domaine & Cas d'Usage | Technologies Clés | Statut / Lien |
| :--- | :--- | :--- | :--- |
| **`Projet01`** | **Retail & Télémétrie Environnementale**<br>_Benchmark Hadoop MapReduce vs PySpark ETL & Analytics_ | PySpark 4, Hadoop, Parquet, Streamlit | 🟢 **Déployé** — [Live App](https://hadoop-pyspark-dashboard.streamlit.app/) / [Documentation](./Projet01_Sales_Pollution_ETL_Hadoop_Spark/) |
| **`Projet02`** | **Pig Latin Dataflow & Analytics**<br>_Pipeline déclaratif et agrégations sur données transactionnelles_ | Apache Pig 0.17, Pig Latin, Hadoop | 🟢 **Terminé** — [Documentation](./Projet02_Pig_Latin_Analytics/) |
| **`Projet03`** | **HiveQL Data Warehouse & Business Intelligence**<br>_Data Warehousing distribué, Window Functions & Studio SQL_ | Apache Hive, HiveQL, DuckDB, Streamlit | 🟢 **Déployé** — [Live App](https://big-data-engineering-workflows-wvurgwswqhwdaraapmxk4a.streamlit.app/) / [Documentation](./Projet03_Hive_Data_Warehouse/) |
| **`Projet04`** | **HBase NoSQL Feature Store & Agentic AI**<br>_Feature Store basse latence, Tool Calling LangGraph & RAG_ | Apache HBase, LangGraph, Mistral AI, ChromaDB | 🟢 **Terminé** — [Documentation](./Projet04_HBase_LangGraph_Agentic_AI/) |

---

## 🛠️ Stack Technique Globale

| Catégorie | Technologies & Outils |
| :--- | :--- |
| **Ingestion & Processing** | `PySpark 4.2.0`, `Apache Hive (HiveQL)`, `Apache Pig (Pig Latin)`, `DuckDB`, `Hadoop MapReduce` |
| **NoSQL & Agentic AI** | `Apache HBase`, `HappyBase`, `LangGraph`, `Mistral AI`, `ChromaDB` |
| **Stockage & Formats** | `Apache Parquet` (Stockage colonne optimisé), `Hive Metastore`, `HDFS` |
| **Data Viz & Dashboard** | `Streamlit 1.40+`, `Plotly Express`, `Pandas` |
| **CI/CD & Deployment** | `Streamlit Cloud`, `Git / GitHub`, `Docker` |
| **Environnement OS** | `Linux (Ubuntu)`, `Bash Scripting` |

---

## 🏗️ Modèle d'Architecture Générique

Chaque workflow de ce dépôt suit un pipeline de données rigoureux et optimisé pour le traitement à grande échelle :

<p align="center">
  <img width="1672" height="941" alt="Architecture Diagram" src="https://github.com/user-attachments/assets/8e0da92a-9b1c-4950-b3a0-ab82f206f517" />
</p>

1. **Extraction & Nettoyage :** Ingestion de fichiers bruts volumineux (logs, transactions CSV/TXT, télémétrie).
2. **ETL Distribué :** Nettoyage, jointures et calculs d'agrégations distribués via **PySpark**, **HiveQL**, **Pig Latin** ou **Hadoop MapReduce**.
3. **Stockage Colonne / NoSQL :** Sauvegarde des données agrégées sous format binaire/compressé (`Parquet`, `Hive External Tables`) ou en table orientée colonnes **HBase** pour servir de Feature Store.
4. **Restitution & Agentic AI :** Publication d'interfaces décisionnelles interactives et agents IA autonomes (LangGraph) capables d'exécuter des requêtes NoSQL via Function Calling.

---

## 🚀 Focus : Applications & Dashboards Déployés

<p align="center">
  <img width="1672" height="941" alt="Dashboard Preview" src="https://github.com/user-attachments/assets/6a797c40-41d8-4b12-b5ca-9bb2aa7cf40e" />
</p>

### 🔗 Liens vers les Applications en Ligne :
* **Projet 01 (Retail & Pollution Analytics) :** 👉 **[Accéder au Tableau de Bord PySpark & Hadoop](https://hadoop-pyspark-dashboard.streamlit.app/)**
* **Projet 03 (HiveQL Data Warehouse & SQL Studio) :** 👉 **[Accéder à la Console HiveQL & Dashboard](https://big-data-engineering-workflows-wvurgwswqhwdaraapmxk4a.streamlit.app/)**

---

## 📂 Structure du Dépôt (Monorepo)

```text
big-data-engineering-workflows/
├── data/                               # Dataset partagé (échantillon léger)
│   └── purchases.txt
├── requirements.txt                    # Dépendances Python globales pour Streamlit Cloud
├── .gitignore                          # Exclusions Git (fichiers bruts > 100 Mo, caches, secrets)
├── README.md                           # Documentation principale du dépôt
│
├── Projet01_Sales_Pollution_ETL_Hadoop_Spark/
│   ├── dashboard/
│   │   └── app.py                      # Application Streamlit du Projet 01
│   ├── data/                           # Résultats Parquet agrégés
│   ├── run_pipeline.sh                 # Script Bash d'exécution de l'ETL
│   └── README.md                       # Documentation détaillée du Projet 01
│
├── Projet02_Pig_Latin_Analytics/
│   ├── scripts/
│   │   └── sales_analytics.pig         # Script Pig Latin d'ETL & agrégation
│   └── README.md                       # Documentation du Projet 02
│
├── Projet03_Hive_Data_Warehouse/
│   ├── dashboard/
│   │   └── app.py                      # Application Streamlit & Console HiveQL
│   ├── scripts/
│   │   ├── 01_create_tables.hql        # Scripts de création de schémas HiveQL
│   │   └── 02_analytical_queries.hql  # Requêtes métiers & Window Functions
│   └── README.md                       # Documentation détaillée du Projet 03
│
└── Projet04_HBase_LangGraph_Agentic_AI/
    ├── agents/
    │   └── rag_graph.py                # Agent LangGraph (Tool Calling & RAG)
    ├── dashboard/
    │   └── app.py                      # Dashboard Streamlit & Agent IA
    ├── hbase/
    │   └── ingest_real_data.py        # Ingestion du Feature Store HBase
    └── README.md                       # Documentation du Projet 04
