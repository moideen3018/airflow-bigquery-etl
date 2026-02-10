# Airflow → BigQuery ETL (Portfolio)

This project demonstrates a simple ETL pipeline using **Apache Airflow** to load events from a JSONL source into **Google BigQuery**.

## Stack
- Python
- Apache Airflow
- Google BigQuery

## BigQuery
- Project: `mohaideen-nizar-data-portfolio`
- Dataset: `my_de_portfolio`
- Table: `github_events` (partitioned by `created_at`)

## Setup (Windows / PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.template .env
