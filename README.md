# 📊 Big Data Engineering Workflows & Business Analytics

[![Live Dashboard](https://img.shields.io/badge/Streamlit_Cloud-Live_App-red?style=for-the-badge&logo=streamlit)](https://hadoop-pyspark-dashboard.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![PySpark](https://img.shields.io/badge/PySpark-4.2.0-orange?style=for-the-badge&logo=apachespark)](https://spark.apache.org/)
[![Apache Pig](https://img.shields.io/badge/Apache_Pig-0.17-orange?style=for-the-badge&logo=apache)](https://pig.apache.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

<p align="center">
  <img width="2172" height="724" alt="Big Data Engineering Banner" src="https://github.com/user-attachments/assets/774e3b6c-b2fd-492a-a01f-d24151507d74" />
</p>

## 📌 Vision & Présentation Globale

Ce dépôt est une suite centralisée de **workflows d'ingénierie Big Data et de tableaux de bord décisionnels**. Il regroupe plusieurs cas d'usage industriels visant à démontrer la transformation de volumes importants de données brutes en **indicateurs métiers à haute valeur ajoutée** grâce à des architectures distribuées modernes (Hadoop, Apache Pig, PySpark, Lakehouse, Streamlit Cloud).

Chaque sous-dossier du dépôt constitue un **projet autonome** disposant de son propre pipeline d'ETL, de son modèle de données et de sa documentation spécifique.

---

## 📚 Catalogue des Projets

| Projet | Domaine & Cas d'Usage | Technologies Clés | Statut / Lien |
| :--- | :--- | :--- | :--- |
| **`Projet01`** | **Retail & Télémétrie Environnementale**<br>_Benchmark Hadoop MapReduce vs PySpark ETL & Analytics_ | PySpark 4, Hadoop, Parquet, Streamlit | 🟢 **Déployé** — [Live App](https://hadoop-pyspark-dashboard.streamlit.app/) / [Documentation](./Projet01_Sales_Pollution_ETL_Hadoop_Spark/) |
| **`Projet02`** | **Pig Latin Dataflow & Analytics**<br>_Pipeline déclaratif et agrégations sur données transactionnelles_ | Apache Pig 0.17, Pig Latin, Hadoop | 🟢 **Terminé** — [Documentation](./Projet02_Pig_Latin_Analytics/) |
| **`Projet03`** | **Streaming & Real-Time Analytics**<br>_Traitement de flux en temps réel_ | Kafka, Spark Streaming, Delta Lake | 🟡 *À venir* |
| **`Projet04`** | **Data Lakehouse & Machine Learning**<br>_Analyse prédictive & Orchestration ETL_ | Delta Lake, Airflow, MLflow | ⚪ *Planifié* |

---

## 🛠️ Stack Technique Globale

| Catégorie | Technologies & Outils |
| :--- | :--- |
| **Ingestion & Processing** | `PySpark 4.2.0`, `Apache Pig (Pig Latin)`, `Hadoop MapReduce`, `Python 3.10+` |
| **Stockage & Formats** | `Apache Parquet` (Stockage en colonnes optimisé), `HDFS` |
| **Data Viz & Dashboard** | `Streamlit 1.60`, `Plotly Express`, `Pandas` |
| **CI/CD & Deployment** | `Streamlit Cloud`, `Git / GitHub` |
| **Environnement OS** | `Linux (Ubuntu)`, `Bash Scripting` |

---

## 🏗️ Modèle d'Architecture Générique

Chaque workflow de ce dépôt suit un pipeline de données rigoureux et optimisé pour le traitement à grande échelle :

<p align="center">
  <img width="1672" height="941" alt="Architecture Diagram" src="https://github.com/user-attachments/assets/8e0da92a-9b1c-4950-b3a0-ab82f206f517" />
</p>

1. **Extraction & Nettoyage :** Ingestion de fichiers bruts volumineux (logs, transactions CSV/TXT, télémétrie).
2. **ETL Distribué :** Nettoyage, jointures et calculs d'agrégations distribués via **PySpark**, **Pig Latin** ou **Hadoop MapReduce**.
3. **Stockage Colonne / Binaire :** Sauvegarde des données agrégées sous format binaire/compressé (`Parquet`, `PigStorage`) pour accélérer les requêtes analytics.
4. **Restitution & Dashboarding :** Publication d'interfaces décisionnelles interactives hébergées sur le Cloud.

---

## 🚀 Focus : Applications & Dashboards Déployés

<p align="center">
  <img width="1672" height="941" alt="Dashboard Preview" src="https://github.com/user-attachments/assets/6a797c40-41d8-4b12-b5ca-9bb2aa7cf40e" />
</p>

### 🔗 Application en ligne (Projet 01)
Accédez directement au tableau de bord de performance E-Commerce & Qualité de l'Air :  
👉 **[Accéder au Tableau de Bord Streamlit Cloud](https://hadoop-pyspark-dashboard.streamlit.app/)**

---

## 📂 Structure du Dépôt (Monorepo)

```text
big-data-engineering-workflows/
├── requirements.txt                   # Dépendances Python globales pour le Cloud
├── .gitignore                         # Exclusions Git (fichiers bruts > 100 Mo, caches)
├── README.md                          # Documentation principale du dépôt
│
├── Projet01_Sales_Pollution_ETL_Hadoop_Spark/
│   ├── dashboard/
│   │   └── app.py                     # Application Streamlit du Projet 01
│   ├── data/                          # Résultats Parquet agrégés issus du pipeline
│   ├── run_pipeline.sh                # Script Bash d'exécution de l'ETL
│   └── README.md                      # Documentation détaillée du Projet 01
│
├── Projet02_Pig_Latin_Analytics/
│   ├── scripts/
│   │   └── sales_analytics.pig        # Script Pig Latin d'ETL & agrégation
│   └── README.md                      # Documentation du Projet 02
│
└── Projet03_.../                      # Prochain projet Big Data (à venir)
