-- ============================================================================
-- Projet 03 : Data Warehousing & ETL avec Apache Hive (HiveQL)
-- Dataset : purchases.txt (TSV: date, time, store, category, cost, payment)
-- ============================================================================

-- 1. Configuration de la session (Optimisations)
SET hive.exec.dynamic.partition = true;
SET hive.exec.dynamic.partition.mode = nonstrict;
SET hive.exec.compress.output = true;

CREATE DATABASE IF NOT EXISTS sales_dw;
USE sales_dw;

-- ----------------------------------------------------------------------------
-- Step 1 : Table Externe (Raw Staging Table) sur les données textuelles brutes
-- ----------------------------------------------------------------------------
CREATE EXTERNAL TABLE IF NOT EXISTS purchases_raw (
    sale_date   STRING,
    sale_time   STRING,
    store_name  STRING,
    category    STRING,
    cost        DOUBLE,
    payment     STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE
LOCATION '/data/raw/purchases';

-- ----------------------------------------------------------------------------
-- Step 2 : Table Managée & Partitionnée au format optimisé ORC
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sales_analytics_orc (
    sale_date   STRING,
    sale_time   STRING,
    category    STRING,
    cost        DOUBLE,
    payment     STRING
)
PARTITIONED BY (store_name STRING)
STORED AS ORC
TBLPROPERTIES ("orc.compress"="SNAPPY");

-- Insertion dynamique avec nettoyage des montants valides
INSERT OVERWRITE TABLE sales_analytics_orc PARTITION (store_name)
SELECT 
    sale_date,
    sale_time,
    category,
    cost,
    payment,
    store_name
FROM purchases_raw
WHERE cost IS NOT NULL AND cost > 0;

-- ----------------------------------------------------------------------------
-- Step 3 : Requêtes Analytics & Window Functions
-- ----------------------------------------------------------------------------

-- KPI 1 : Chiffre d'affaires global et total des transactions par magasin
SELECT 
    store_name,
    ROUND(SUM(cost), 2) AS total_sales,
    COUNT(1) AS transaction_count
FROM sales_analytics_orc
GROUP BY store_name
ORDER BY total_sales DESC;

-- KPI 2 : Top 3 des meilleures catégories de produits par magasin (Window Function)
WITH ranked_categories AS (
    SELECT 
        store_name,
        category,
        ROUND(SUM(cost), 2) AS category_sales,
        ROW_NUMBER() OVER (PARTITION BY store_name ORDER BY SUM(cost) DESC) AS rank
    FROM sales_analytics_orc
    GROUP BY store_name, category
)
SELECT 
    store_name,
    category,
    category_sales
FROM ranked_categories
WHERE rank <= 3;