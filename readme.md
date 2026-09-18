# MeteoriSK

## Overview
MeteoriSK is an automated data engineering pipeline designed to help logistics and delivery teams in Morocco anticipate weather-related disruptions. By ingesting multi-day meteorological forecasts and geographical data, the system calculates a specialized weather risk score for various cities, allowing operational managers to adapt delivery schedules to adverse conditions like heavy rain, high winds, or extreme temperatures.

## Architecture
The project follows a Medallion data architecture (Bronze, Silver, Gold) orchestrated by Apache Airflow:

* **Bronze (Ingestion):** Extracts raw Moroccan city coordinates from a static dataset and fetches daily weather forecasts from the Open-Meteo API. Data is stored in its original format.
* **Silver (Transformation):** Cleans the raw data, standardizes data types, handles missing values, and merges the geographical and meteorological datasets.
* **Gold (Feature Engineering):** Applies business logic to categorize weather conditions and calculates a weighted weather risk score (0-100). The final dataset is loaded into a relational database.

## Technical Stack
* **Orchestration:** Apache Airflow
* **Processing:** Python, Pandas
* **Database:** PostgreSQL (managed via SQLAlchemy ORM)
* **Visualization:** Streamlit, Plotly
* **Infrastructure:** Docker & Docker Compose

## Core Features
* **Automated ETL:** Scheduled DAG execution with built-in retry mechanisms and failure handling.
* **Incremental Loading:** Uses database merge operations to update current forecasts while preventing duplicate records.
* **Interactive Dashboard:** A Streamlit interface connected directly to the PostgreSQL database, featuring an interactive Plotly map and dynamic filtering for operational analysis.
* **Containerized Environment:** The entire stack (Airflow, Postgres, Streamlit) runs in isolated Docker containers for consistent deployment across environments.