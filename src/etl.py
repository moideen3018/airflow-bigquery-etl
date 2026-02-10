import json
from datetime import datetime, timezone
from typing import Dict, List

from google.cloud import bigquery

def parse_event(line: str) -> Dict:
    obj = json.loads(line)

    event_id = str(obj.get("id"))
    event_type = obj.get("type", "Unknown")
    actor_login = (obj.get("actor") or {}).get("login")
    repo_name = (obj.get("repo") or {}).get("name")
    created_at = obj.get("created_at")

    if not event_id or not created_at or not event_type:
        raise ValueError("Missing required fields: id/type/created_at")

    return {
        "event_id": event_id,
        "event_type": event_type,
        "actor_login": actor_login,
        "repo_name": repo_name,
        "created_at": created_at,  # BigQuery parser
        "raw": obj,
        "ingested_at": datetime.now(timezone.utc).isoformat(),
    }

def load_events_from_jsonl(path: str) -> List[Dict]:
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(parse_event(line))
    return rows

def upsert_to_bigquery(
    client: bigquery.Client,
    dataset_id: str,
    table_id: str,
    rows: List[Dict],
) -> int:
    if not rows:
        return 0

    table = f"{client.project}.{dataset_id}.{table_id}"
    errors = client.insert_rows_json(table, rows)
    if errors:
        raise RuntimeError(f"BigQuery insert errors: {errors}")
    return len(rows)
