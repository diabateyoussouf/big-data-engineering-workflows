import happybase
import pandas as pd

HBASE_HOST = "localhost"
HBASE_PORT = 9090
TABLE_NAME = "retail_feature_store"

def inspect_hbase_records():
    connection = happybase.Connection(host=HBASE_HOST, port=HBASE_PORT)
    connection.open()
    table = connection.table(TABLE_NAME)

    records = []
    # Parcours des enregistrements dans HBase (Scan)
    for row_key, data in table.scan():
        row_dict = {"city (RowKey)": row_key.decode("utf-8")}
        for col_name, val in data.items():
            row_dict[col_name.decode("utf-8")] = val.decode("utf-8")
        records.append(row_dict)

    connection.close()
    
    df_result = pd.DataFrame(records)
    print("\n=== APERÇU DES DONNÉES RÉELLES DANS HBASE ===")
    print(df_result.head(10).to_string(index=False))

if __name__ == "__main__":
    inspect_hbase_records()