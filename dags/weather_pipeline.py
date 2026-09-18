from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator

from transformation.cleaning import transform_weather_data
from transformation.gold_transformation import transform_weather_data_gold
from sql.create_table import load_data_to_postgres
from extraction.extract_weather import extract_weather_data
    
default_args = {
    'owner': 'airflow',
    'retries': 5,
    'retry_delay': 300,
}

with DAG(
    dag_id='weather_pipeline',
    description='A DAG to process weather data and store it in a PostgreSQL database',
    default_args=default_args, 
    schedule_interval='@daily',
    start_date=datetime(2026, 9, 17),
    catchup=False
) as dag:

    extraction_task = PythonOperator(
        task_id='extract_weather_data',
        python_callable=extract_weather_data
    )

    transformation_task = PythonOperator(
        task_id='transform_weather_data',
        python_callable=transform_weather_data
    )

    gold_transformation_task = PythonOperator(
        task_id='transform_weather_data_gold',
        python_callable=transform_weather_data_gold
    )

    load_data_task = PythonOperator(
        task_id='load_data_to_postgres',
        python_callable=load_data_to_postgres
    )

    extraction_task >> transformation_task >> gold_transformation_task >> load_data_task