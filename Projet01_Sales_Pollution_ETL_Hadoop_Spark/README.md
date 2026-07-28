# ⚡ Modernisation d'Architecture Big Data : De MapReduce à PySpark

Projet d'ingénierie de données visant à transformer des pipelines de traitement batch legacy **Hadoop MapReduce (Python Streaming)** vers une architecture moderne **PySpark DataFrames / Parquet** avec restitution décisionnelle via **Streamlit & Plotly**.

---

## 🏛️ Architecture du Pipeline

```text
[Données Brutes (Data Lake / HDFS)]
       │
       ├──> 🐘 Legacy Layer : MapReduce (Python 3 Streaming)
       │       └── Validation bas-niveau (Key-Value Aggregations)
       │
       └──> ⚡ Modern Layer : PySpark ETL (In-Memory DataFrames)
               ├── Nettoyage & Typage structuré
               ├── Analyses Statistiques & Corrélations (Pearson r)
               └── 📦 Storage Layer : Fichiers Parquet Compressés
                       │
                       └──> 📊 Serving Layer : Dashboard Interactif Streamlit


🛠️ Tech Stack & Outils
Gestionnaire d'environnement : uv (Fast Python Package Installer)

Traitement Distributed / Batch : PySpark 3.x, Hadoop Streaming (Python 3)

Format de Stockage Optimisé : Apache Parquet (Columnar Storage)

Serving / UI : Streamlit, Plotly Express

Versioning : Git (Workflow par branche dédiée feature/projet01-sales-pollution-etl)

📁 Structure du Projet:
Projet01_Sales_Pollution_ETL_Hadoop_Spark/
├── data/                       # Données brutes et exports Parquet
├── mapreduce/                  # Scripts Hadoop Streaming (Mappers & Reducers)
│   ├── mapper_sales.py
│   ├── reducer_sales.py
│   ├── mapper_pollution.py
│   └── reducer_pollution.py
├── pyspark/                    # Pipelines PySpark DataFrames
│   ├── sales_etl.py
│   └── pollution_etl.py
├── dashboard/                  # Application Web Streamlit
│   └── app.py
├── run_pipeline.sh             # Script d'orchestration globale
├── pyproject.toml / uv.lock    # Dépendances du projet
└── README.md