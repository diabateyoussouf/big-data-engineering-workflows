from pyspark.sql import SparkSession

# 1. Initialiser la session Spark (Moteur SQL compatible HiveQL)
spark = SparkSession.builder \
    .appName("HiveQL_Local_Testing") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

print("⚡ Moteur Spark SQL/HiveQL prêt.\n")

# 2. Ingestion du dataset brut purchases.txt
data_path = "../data/purchases.txt"  # Adapte le chemin si nécessaire

df_raw = spark.read.option("delimiter", "\t").csv(
    data_path, 
    inferSchema=True
).toDF("sale_date", "sale_time", "store_name", "category", "cost", "payment")

# 3. Créer une vue temporaire interrogeable en HiveQL
df_raw.createOrReplaceTempView("purchases_raw")

# ----------------------------------------------------------------------------
# Requête HiveQL 1 : Chiffre d'Affaires & Transactions par Magasin
# ----------------------------------------------------------------------------
hive_query_1 = """
SELECT 
    store_name,
    ROUND(SUM(cost), 2) AS total_sales,
    COUNT(1) AS transaction_count
FROM purchases_raw
WHERE cost IS NOT NULL AND cost > 0
GROUP BY store_name
ORDER BY total_sales DESC
"""

print("📊 --- KPI 1 : Ventes par Magasin (HiveQL) ---")
spark.sql(hive_query_1).show(10, truncate=False)

# ----------------------------------------------------------------------------
# Requête HiveQL 2 : Top Catégories par Magasin (Window Function)
# ----------------------------------------------------------------------------
hive_query_2 = """
WITH ranked_categories AS (
    SELECT 
        store_name,
        category,
        ROUND(SUM(cost), 2) AS category_sales,
        ROW_NUMBER() OVER (PARTITION BY store_name ORDER BY SUM(cost) DESC) AS rank
    FROM purchases_raw
    WHERE cost IS NOT NULL AND cost > 0
    GROUP BY store_name, category
)
SELECT store_name, category, category_sales
FROM ranked_categories
WHERE rank <= 3
"""

print("🏆 --- KPI 2 : Top 3 Catégories par Magasin (HiveQL Window Function) ---")
spark.sql(hive_query_2).show(15, truncate=False)

spark.stop()