from google.cloud import bigquery

def get_bq_client(project_id: str) -> bigquery.Client:
    # GOOGLE_APPLICATION_CREDENTIALS
    return bigquery.Client(project=project_id)

def ensure_table(client: bigquery.Client, dataset_id: str, table_id: str) -> bigquery.Table:
    dataset_ref = bigquery.DatasetReference(client.project, dataset_id)
    table_ref = dataset_ref.table(table_id)

    schema = [
        bigquery.SchemaField("event_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("event_type", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("actor_login", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("repo_name", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("created_at", "TIMESTAMP", mode="REQUIRED"),
        bigquery.SchemaField("raw", "JSON", mode="REQUIRED"),
        bigquery.SchemaField("ingested_at", "TIMESTAMP", mode="REQUIRED"),
    ]

    try:
        return client.get_table(table_ref)
    except Exception:
        table = bigquery.Table(table_ref, schema=schema)
        table.time_partitioning = bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY,
            field="created_at",
        )
        return client.create_table(table)
