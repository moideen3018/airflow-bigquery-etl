from google.cloud import bigquery
from src.config import get_settings
from src.bq import ensure_table

def main():
    s = get_settings()
    client = bigquery.Client(project=s.project_id)

    dataset_ref = bigquery.Dataset(f"{s.project_id}.{s.dataset_id}")
    dataset_ref.location = "EU"
    try:
        client.get_dataset(dataset_ref)
        print("Dataset exists:", s.dataset_id)
    except Exception:
        client.create_dataset(dataset_ref)
        print("Created dataset:", s.dataset_id)

    table = ensure_table(client, s.dataset_id, s.table_id)
    print("Table ready:", table.full_table_id)

if __name__ == "__main__":
    main()
