#!/usr/bin/env python3
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, date_format, max as spark_max, min as spark_min, sum as spark_sum, avg, count, to_date

def run_sales_etl():
    # 1. Initialisation de la SparkSession
    spark = SparkSession.builder \
        .appName("Retail_Sales_ETL") \
        .master("local[*]") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")

    # 2. Chargement du fichier purchases.txt
    df = spark.read.option("delimiter", "\t") \
        .csv("data/purchases.txt") \
        .toDF("date", "time", "store", "category", "cost", "payment")
    
    # Casting du coût en valeur numérique
    df = df.withColumn("cost", col("cost").cast("double")) \
           .withColumn("parsed_date", to_date(col("date"), "yyyy-MM-dd"))

    print("=== 📊 Aperçu des données brutes Ventes ===")
    df.show(5)

    # A. Ventes totales par magasin
    sales_by_store = df.groupBy("store").agg(spark_sum("cost").alias("total_sales"))
    
    # B. Ventes Min et Max par magasin (Reno, Toledo, Chandler)
    min_max_by_store = df.groupBy("store").agg(
        spark_min("cost").alias("min_sale"),
        spark_max("cost").alias("max_sale")
    )

    # C. Ventes par catégorie de produits (Ex: Toys, Consumer Electronics)
    sales_by_category = df.groupBy("category").agg(spark_sum("cost").alias("total_sales"))

    # D. Somme et Moyenne des ventes par jour de la semaine
    sales_by_day = df.withColumn("day_of_week", date_format(col("parsed_date"), "EEEE")) \
                     .groupBy("day_of_week") \
                     .agg(
                         spark_sum("cost").alias("total_sales"),
                         avg("cost").alias("avg_sales"),
                         count("cost").alias("transaction_count")
                     )

    print("=== 🛍️ Ventes par jour de la semaine ===")
    sales_by_day.show()

    # E. Export des résultats agrégés pour le Dashboard (Serving Layer)
    sales_by_store.write.mode("overwrite").parquet("data/processed_sales_by_store.parquet")
    sales_by_category.write.mode("overwrite").parquet("data/processed_sales_by_category.parquet")
    sales_by_day.write.mode("overwrite").parquet("data/processed_sales_by_day.parquet")

    print("✅ Pipeline PySpark Sales exécuté avec succès. Données exportées au format Parquet.")
    spark.stop()

if __name__ == "__main__":
    run_sales_etl()