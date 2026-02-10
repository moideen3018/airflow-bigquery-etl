import os
import requests
from datetime import datetime
from google.cloud import bigquery
from google.oauth2 import service_account

# -----------------------------
# CONFIG
# -----------------------------
GITHUB_EVENTS_URL = "https://api.github.com/events"
PROJECT_ID = os.getenv("GCP_PROJECT_ID")
DATASET_ID = os.getenv("BQ_DATASET")
TABLE_ID = os.getenv("BQ_TABLE")
SERVICE_ACCOUNT_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# -----------------------------
# BIGQUERY CLIENT
# -----------------------------
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_PATH
)

bq_client = bigquery.Client(
    credentials=credentials,
    project=PROJECT_ID
)

# -----------------------------
# EXTRACT
# -----------------------------
def fetch_github_events(limit=30):
    response = requests.get(GITHUB_EVENTS_URL)
    response.raise_for_status()
    return response.json()[:limit]

# -----------------------------
# TRANSFORM
# -----------------------------
def transform_events(events):
    transformed = []

    for event in events:
        transformed.append({
            "event_id": event.get("id"),
            "event_type": event.get("type"),
            "repo_name": event.get("repo", {}).get("name"),
            "actor_login": event.get("actor", {}).get("login"),
            "created_at": event.get("created_at"),
            "ingested_at": datetime.utcnow().isoformat()
        })

    return transformed

# -----------------------------
# LOAD
# -----------------------------
def load_to_bigquery(rows):
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    errors = bq_client.insert_rows_json(table_ref, rows)

    if errors:
        raise RuntimeError(f"BigQuery insert errors: {errors}")

    print(f"Loaded {len(rows)} rows into {table_ref}")

# -----------------------------
# MAIN
# -----------------------------
def run_pipeline():
    events = fetch_github_events()
    clean_rows = transform_events(events)
    load_to_bigquery(clean_rows)

if __name__ == "__main__":
    run_pipeline()
