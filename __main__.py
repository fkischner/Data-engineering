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

def run_etl(api_key, provinces, conn):
    data = fetch_data_from_api(api_key, provinces)
    if data:
        df = transform_data(data)
        success = load_data_to_redshift(df, conn)
        if success:
            print("Datos de todas las provincias cargados exitosamente en Redshift")
        else:
            print("No se pudieron cargar los datos de las provincias en Redshift")
    else:
        print("No se pudieron obtener datos de la API para las provincias")

if __name__ == "__main__":
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
    run_sql_file("create_table.sql", conn)
    run_etl(api_key, provinces, conn)
    conn.close()