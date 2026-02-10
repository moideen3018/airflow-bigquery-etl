from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Add project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.etl.github_to_bq import run_pipeline

default_args = {
    "owner": "data-engineering",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="github_events_to_bigquery",
    default_args=default_args,
    description="ETL GitHub public events into BigQuery",
    schedule_interval="@daily",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["github", "bigquery", "etl"],
) as dag:

    etl_task = PythonOperator(
        task_id="run_github_etl",
        python_callable=run_pipeline
    )

    etl_task
