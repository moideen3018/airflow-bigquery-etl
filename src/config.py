import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()  # loads .env if present

@dataclass(frozen=True)
class Settings:
    project_id: str = os.getenv("GCP_PROJECT_ID", "")
    dataset_id: str = os.getenv("BQ_DATASET_ID", "")
    table_id: str = os.getenv("BQ_TABLE_ID", "")
    credentials_path: str = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")

def get_settings() -> Settings:
    s = Settings()
    missing = [k for k, v in s.__dict__.items() if not v]
    if missing:
        raise RuntimeError(f"Missing env vars in .env: {missing}")
    return s
