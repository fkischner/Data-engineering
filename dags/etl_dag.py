import sys
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# Ajustar el PYTHONPATH si es necesario
sys.path.insert(0, '/usr/local/airflow/Modules')

# Importar las funciones del ETL
from extract import fetch_data_from_api
from transform import transform_data
from load import load_data_to_redshift

# Definir los argumentos por defecto del DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 7, 5),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Definir el DAG
dag = DAG(
    'etl_dag',
    default_args=default_args,
    description='Dag diario',
    schedule_interval=timedelta(days=1),
)

# Definir las funciones para las tareas
def run_etl():
    # Lógica para ejecutar ETL
    fetch_data_from_api()
    transform_data()
    load_data_to_redshift()

# Definir las tareas
run_etl_task = PythonOperator(
    task_id='run_etl',
    python_callable=run_etl,
    dag=dag,
)

# Definir el flujo de las tareas
run_etl_task