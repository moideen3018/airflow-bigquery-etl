# GitHub Events ETL Pipeline (Airflow → BigQuery)

## Overview
This project implements an end-to-end cloud ETL pipeline that ingests public GitHub event data,
transforms raw JSON into analytics-ready format, and loads it into Google BigQuery.
The pipeline is designed following production-grade data engineering practices,
including secure authentication, modular ETL logic, and workflow orchestration.

## Architecture
GitHub API → Python ETL → Apache Airflow → Google BigQuery

## Tech Stack
- Python
- Apache Airflow
- Google BigQuery
- Google Cloud IAM (Service Accounts)
- REST APIs

## Data Pipeline
1. Extract public GitHub events using the GitHub REST API  
2. Transform nested JSON data into structured, analytics-ready records  
3. Load processed data into Google BigQuery tables  
4. Orchestrate and schedule the pipeline using Apache Airflow  

## Data Model
The BigQuery table stores key event attributes including:
- Event ID
- Event type
- Repository name
- Actor username
- Event timestamp
- Ingestion timestamp

This schema supports downstream analytics and reporting use cases.

## What This Demonstrates
- Secure cloud authentication using GCP service accounts and environment variables
- End-to-end ETL pipeline design using Python
- Workflow orchestration and scheduling with Apache Airflow
- Analytics-ready data modeling in a cloud data warehouse
- Clean, modular, and maintainable project structure

## How to Run Locally
1. Create and activate a virtual environment  
2. Configure environment variables using `.env` (see `.env.sample`)  
3. Run the ETL pipeline:

```bash
python src/etl/github_to_bq.py
