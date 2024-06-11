# Importaciones desde el paquete Modules
from Modules.extract import fetch_data_from_api
from Modules.transform import transform_data
from Modules.load import load_data_to_redshift
import psycopg2
from dotenv import load_dotenv
import os

def run_sql_file(file_path, connection):
    with open(file_path, 'r') as file:
        sql_script = file.read()
    cursor = connection.cursor()
    try:
        cursor.execute(sql_script)
        connection.commit()
        print("SQL script executed successfully.")
    except Exception as e:
        print("Error executing SQL script:", e)
    finally:
        cursor.close()

def run_etl(api_key):
    city = 'Buenos Aires'
    data = fetch_data_from_api(api_key, city)
    if data:
        df = transform_data(data)
        success = load_data_to_redshift(df)
        if success:
            print("Datos de Buenos Aires cargados exitosamente en Redshift")
        else:
            print("No se pudieron cargar los datos de Buenos Aires en Redshift")
    else:
        print("No se pudieron obtener datos de la API para Buenos Aires")

if __name__ == "__main__":
    # Cargar variables de entorno desde el archivo .env
    load_dotenv()
    api_key = 'dfe405e778a45bc7c92510e939bebef7'
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
    run_sql_file("create_table.sql", conn)
    run_etl(api_key)
    conn.close()