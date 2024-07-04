from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import sys
import os

# Añadir el directorio de trabajo a sys.path
sys.path.append('/usr/local/airflow/Modules')

# Importar las funciones del ETL
from extract import fetch_data_from_api
from transform import transform_data
from load import load_data_to_redshift
import psycopg2
from dotenv import load_dotenv

def run_etl():
    load_dotenv()
    api_key = os.getenv('OPENWEATHER_API_KEY')
    provinces = ["Buenos Aires", "Catamarca", "Chaco", "Chubut", "Córdoba", "Corrientes", "Entre Ríos", "Formosa", "Jujuy", "La Pampa", "La Rioja", "Mendoza", "Misiones", "Neuquén", "Río Negro", "Salta", "San Juan", "San Luis", "Santa Cruz", "Santa Fe", "Santiago del Estero", "Tierra del Fuego", "Tucumán"]
    dbname = os.getenv('REDSHIFT_DBNAME')
    user = os.getenv('REDSHIFT_USERNAME')
    password = os.getenv('REDSHIFT_PASSWORD')
    host = os.getenv('REDSHIFT_HOST')
    port = os.getenv('REDSHIFT_PORT')

    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )

    run_sql_file("/create_table.sql", conn)
    run_etl(api_key, provinces, conn)
    conn.close()

def run_sql_file(file_path, connection):
    with open(file_path, 'r') as file:
        sql_script = file.read()
    cursor = connection.cursor()
    try:
        cursor.execute(sql_script)
        connection.commit()
    except Exception as e:
        connection.rollback()
    finally:
        cursor.close()

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'etl_dag',
    default_args=default_args,
    description='ETL DAG',
    schedule_interval=timedelta(days=1),
)

run_etl_task = PythonOperator(
    task_id='run_etl',
    python_callable=run_etl,
    dag=dag,
)

run_etl_task