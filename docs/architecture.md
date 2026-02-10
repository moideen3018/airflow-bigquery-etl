# Architecture Overview

This project implements a cloud-based ETL pipeline designed for analytics workloads.

## Components
- GitHub Public API (Data Source)
- Python ETL Layer
- Apache Airflow (Orchestration)
- Google BigQuery (Data Warehouse)

## Design Considerations
- Secure authentication via GCP service accounts
- Idempotent data loading
- Modular, maintainable code structure
