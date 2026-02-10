import os
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.config import get_settings
from src.bq import get_bq_client, ensure_table
from src.etl import load_events_from_jsonl, upsert_to_bigquery

def run_etl():
    s = get_settings()
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = s.credentials_path

    client = get_bq_client(s.project_id)
    ensure_table(client, s.dataset_id, s.table_id)

    rows = load_events_from_jsonl("data/sample_events.jsonl")
    inserted = upsert_to_bigquery(client, s.dataset_id, s.table_id, rows)
    print(f"Inserted {inserted} rows into {s.dataset_id}.{s.table_id}")

with DAG(
    dag_id="etl_github_events_to_bq",
    start_date=datetime(2026, 2, 1),
    schedule=None,   # manual trigger
    catchup=False,
    tags=["portfolio", "bigquery", "etl"],
) as dag:
    task_run = PythonOperator(
        task_id="run_etl",
        python_callable=run_etl,
    )
