import happybase
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("HBaseIngest")

HBASE_HOST = "localhost"
HBASE_PORT = 9090
TABLE_NAME = "customer_feature_store"

def init_hbase_feature_store():
    try:
        connection = happybase.Connection(host=HBASE_HOST, port=HBASE_PORT)
        connection.open()
        logger.info(f"Connecté au serveur HBase sur {HBASE_HOST}:{HBASE_PORT}")

        tables = [t.decode("utf-8") for t in connection.tables()]
        
        # Supprimer la table si elle existe déjà pour réinitialiser
        if TABLE_NAME in tables:
            logger.info(f"Suppression de la table existante {TABLE_NAME}...")
            connection.disable_table(TABLE_NAME)
            connection.delete_table(TABLE_NAME)

        # Création des Column Families (info, metrics, risk)
        connection.create_table(
            TABLE_NAME,
            {
                "info": dict(max_versions=1),
                "metrics": dict(max_versions=3),  # Garde l'historique des 3 dernières valeurs
                "risk": dict(max_versions=1)
            }
        )
        logger.info(f"Table HBase '{TABLE_NAME}' créée avec succès.")

        table = connection.table(TABLE_NAME)

        # Insertion de données de test dans le Feature Store
        sample_customers = {
            b"usr_1001": {
                b"info:name": b"Alice Dupont",
                b"info:segment": b"VIP",
                b"info:country": b"FR",
                b"metrics:total_spent": b"4250.80",
                b"metrics:avg_basket": b"141.69",
                b"metrics:orders_cnt": b"30",
                b"risk:churn_score": b"0.12",
                b"risk:fraud_flag": b"false"
            },
            b"usr_1002": {
                b"info:name": b"Bob Smith",
                b"info:segment": b"Standard",
                b"info:country": b"US",
                b"metrics:total_spent": b"310.00",
                b"metrics:avg_basket": b"62.00",
                b"metrics:orders_cnt": b"5",
                b"risk:churn_score": b"0.78",
                b"risk:fraud_flag": b"false"
            },
            b"usr_1003": {
                b"info:name": b"Charlie Lee",
                b"info:segment": b"Inactif",
                b"info:country": b"CA",
                b"metrics:total_spent": b"12.50",
                b"metrics:avg_basket": b"12.50",
                b"metrics:orders_cnt": b"1",
                b"risk:churn_score": b"0.95",
                b"risk:fraud_flag": b"true"
            }
        }

        with table.batch() as b:
            for row_key, data in sample_customers.items():
                b.put(row_key, data)

        logger.info(f"{len(sample_customers)} profils clients ingérés dans HBase.")
        connection.close()

    except Exception as e:
        logger.error(f"Erreur lors de l'interaction avec HBase : {e}")

if __name__ == "__main__":
    init_hbase_feature_store()