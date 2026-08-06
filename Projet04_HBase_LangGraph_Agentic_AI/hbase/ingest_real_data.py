import os
import happybase
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("HBaseRealIngest")

HBASE_HOST = "localhost"
HBASE_PORT = 9090
TABLE_NAME = "retail_feature_store"
DATA_PATH = "data/purchases.txt"

def process_and_ingest_purchases():
    if not os.path.exists(DATA_PATH):
        logger.error(f"Fichier introuvable : {DATA_PATH}. Assurez-vous d'avoir l'échantillon dans data/")
        return

    logger.info(f"Chargement et traitement du fichier réel {DATA_PATH}...")
    
    # Lecture des données réelles (séparateur tabulation)
    columns = ["date", "time", "city", "category", "amount", "payment"]
    df = pd.read_csv(DATA_PATH, sep="\t", names=columns, header=None)
    
    # Nettoyage et conversion des types
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)
    df["city"] = df["city"].astype(str).str.strip()
    df["category"] = df["category"].astype(str).str.strip()
    df["payment"] = df["payment"].astype(str).str.strip()

    logger.info(f"Calcul des indicateurs agrégés sur {len(df):,} transactions réelles...")

    # Connexion à HBase via Thrift
    connection = happybase.Connection(host=HBASE_HOST, port=HBASE_PORT)
    connection.open()
    tables = [t.decode("utf-8") for t in connection.tables()]

    # Réinitialisation de la table si elle existe
    if TABLE_NAME in tables:
        connection.disable_table(TABLE_NAME)
        connection.delete_table(TABLE_NAME)

    connection.create_table(
        TABLE_NAME,
        {
            "sales": dict(max_versions=1),
            "categories": dict(max_versions=1),
            "payments": dict(max_versions=1)
        }
    )
    table = connection.table(TABLE_NAME)

    # Groupement par Ville (RowKey) pour générer les vecteurs de métriques
    grouped = df.groupby("city")
    
    with table.batch() as b:
        for city, group in grouped:
            if not city or city == "nan":
                continue

            total_rev = group["amount"].sum()
            avg_tx = group["amount"].mean()
            tx_cnt = len(group)

            # Catégorie générant le plus de revenu dans la ville
            cat_summary = group.groupby("category")["amount"].sum()
            top_cat = cat_summary.idxmax() if not cat_summary.empty else "N/A"
            top_cat_rev = cat_summary.max() if not cat_summary.empty else 0.0

            # Répartition des modes de paiement
            pmt_counts = group["payment"].value_counts().to_dict()
            cash_cnt = pmt_counts.get("Cash", 0)
            card_cnt = pmt_counts.get("Visa", 0) + pmt_counts.get("MasterCard", 0)
            paypal_cnt = pmt_counts.get("PayPal", 0)

            # Assemblage des familles de colonnes
            row_key = city.encode("utf-8")
            data = {
                b"sales:total_revenue": str(round(total_rev, 2)).encode("utf-8"),
                b"sales:avg_transaction": str(round(avg_tx, 2)).encode("utf-8"),
                b"sales:transaction_count": str(tx_cnt).encode("utf-8"),
                b"categories:top_category": str(top_cat).encode("utf-8"),
                b"categories:top_category_revenue": str(round(top_cat_rev, 2)).encode("utf-8"),
                b"payments:cash_count": str(cash_cnt).encode("utf-8"),
                b"payments:card_count": str(card_cnt).encode("utf-8"),
                b"payments:paypal_count": str(paypal_cnt).encode("utf-8"),
            }
            b.put(row_key, data)

    logger.info(f"✅ Ingestion terminée avec succès : {len(grouped)} villes insérées dans HBase.")
    connection.close()

if __name__ == "__main__":
    process_and_ingest_purchases()