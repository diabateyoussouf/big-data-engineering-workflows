-- ============================================================================
-- Projet 02 : Data Analytics & ETL avec Apache Pig & Pig Latin
-- Dataset : purchases.txt (Format TSV : date, time, store, category, cost, payment)
-- ============================================================================

-- 1. Chargement et typage des données brutes
purchases = LOAD 'data/purchases.txt' USING PigStorage('\t') 
    AS (
        date:chararray, 
        time:chararray, 
        store:chararray, 
        category:chararray, 
        cost:double, 
        payment:chararray
    );

-- 2. Nettoyage : filtrer les transactions invalides ou nulles
cleaned_purchases = FILTER purchases BY cost IS NOT NULL AND cost > 0;

-- ----------------------------------------------------------------------------
-- KPI 1 : Chiffre d'Affaires et Volume par Magasin
-- ----------------------------------------------------------------------------
grouped_by_store = GROUP cleaned_purchases BY store;

sales_by_store = FOREACH grouped_by_store GENERATE 
    group AS store, 
    ROUND_TO(SUM(cleaned_purchases.cost), 2) AS total_sales,
    COUNT(cleaned_purchases) AS total_transactions;

-- Sauvegarde du résultat
STORE sales_by_store INTO 'output/sales_by_store' USING PigStorage(',');

-- ----------------------------------------------------------------------------
-- KPI 2 : Top Catégories Produits (Tri par CA décroissant)
-- ----------------------------------------------------------------------------
grouped_by_category = GROUP cleaned_purchases BY category;

sales_by_category = FOREACH grouped_by_category GENERATE 
    group AS category, 
    ROUND_TO(SUM(cleaned_purchases.cost), 2) AS total_sales;

sorted_categories = ORDER sales_by_category BY total_sales DESC;

-- Sauvegarde du résultat
STORE sorted_categories INTO 'output/sales_by_category' USING PigStorage(',');