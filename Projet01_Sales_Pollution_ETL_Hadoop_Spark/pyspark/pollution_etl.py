#!/usr/bin/env python3
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum, corr, max as spark_max

def run_pollution_etl():
    spark = SparkSession.builder \
        .appName("Environmental_Pollution_ETL") \
        .master("local[*]") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")

    # 1. Chargement des données de pollution avec en-tête
    df = spark.read.option("header", "true") \
        .option("delimiter", "\t") \
        .csv("data/AirPollution.txt")

    # Casting des colonnes numériques
    df = df.withColumn("CO", col("CO").cast("double")) \
           .withColumn("O3", col("O3").cast("double")) \
           .withColumn("Temperature", col("Temperature").cast("double")) \
           .withColumn("Mois", col("Mois").cast("int"))

    print("=== 🌍 Aperçu des données de Pollution ===")
    df.show(5)

    # A. Total des concentrations de CO par ville et par mois
    co_by_city_month = df.groupBy("Ville", "Mois") \
                         .agg(spark_sum("CO").alias("Total_CO")) \
                         .orderBy("Ville", "Mois")

    # B. Ville enregistrant la concentration maximale de O3
    max_o3_val = df.select(spark_max("O3")).collect()[0][0]
    city_max_o3 = df.filter(col("O3") == max_o3_val).select("Ville", "Mois", "O3")
    print("=== 🚨 Ville(s) avec concentration maximale en O3 ===")
    city_max_o3.show()

    # C. Mois dont la température est comprise entre 30°C et 40°C
    filtered_temp = df.filter((col("Temperature") >= 30) & (col("Temperature") <= 40)) \
                      .select("Ville", "Mois", "Temperature") \
                      .distinct()

    # D. Calcul du coefficient de corrélation (Pearson) entre Poluants et Température
    r_co_temp = df.stat.corr("CO", "Temperature")
    r_o3_temp = df.stat.corr("O3", "Temperature")

    print(f"📈 Coefficient de corrélation r(CO, Température) : {r_co_temp:.4f}")
    print(f"📈 Coefficient de corrélation r(O3, Température) : {r_o3_temp:.4f}")

    # E. Export pour la couche Serving
    co_by_city_month.write.mode("overwrite").parquet("data/processed_co_monthly.parquet")
    df.write.mode("overwrite").parquet("data/processed_pollution_full.parquet")

    print("✅ Pipeline PySpark Pollution exécuté avec succès.")
    spark.stop()

if __name__ == "__main__":
    run_pollution_etl()