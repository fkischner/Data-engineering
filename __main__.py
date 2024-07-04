# Importaciones desde el paquete Modules
from Modules.extract import fetch_data_from_api  # Función para obtener datos desde una API
from Modules.transform import transform_data     # Función para transformar los datos obtenidos
from Modules.load import load_data_to_redshift   # Función para cargar datos en Redshift
import psycopg2                                  # Biblioteca para conectarse a bases de datos PostgreSQL
from dotenv import load_dotenv                   # Biblioteca para cargar variables de entorno desde un archivo .env
import os                                        # Biblioteca para interactuar con el sistema operativo

def run_sql_file(file_path, connection):
    """
    Función para ejecutar un script SQL desde un archivo.

    Args:
    - file_path: Ruta del archivo SQL.
    - connection: Objeto de conexión a la base de datos.

    """
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
    """
    Función principal del proceso ETL (Extract, Transform, Load).

    Args:
    - api_key: Clave de API para obtener datos.
    - provinces: Lista de provincias para las cuales obtener datos.
    - conn: Objeto de conexión a la base de datos Redshift.

    """
    # Extracción de datos desde la API
    data = fetch_data_from_api(api_key, provinces)
    if data:
        # Transformación de los datos obtenidos
        df = transform_data(data)
        # Carga de los datos transformados a Redshift
        success = load_data_to_redshift(df, conn)
        if success:
            print("Datos de todas las provincias cargados exitosamente en Redshift")
        else:
            print("No se pudieron cargar los datos de las provincias en Redshift")
    else:
        print("No se pudieron obtener datos de la API para las provincias")

if __name__ == "__main__":
    # Cargar variables de entorno desde un archivo .env
    load_dotenv()
    
    # Obtener la clave de API desde las variables de entorno
    api_key = os.getenv('OPENWEATHER_API_KEY')
    
    # Lista de provincias para las cuales se obtendrán datos
    provinces = ["Buenos Aires", "Catamarca", "Chaco", "Chubut", "Córdoba", "Corrientes", "Entre Ríos", "Formosa", "Jujuy", "La Pampa", "La Rioja", "Mendoza", "Misiones", "Neuquén", "Río Negro", "Salta", "San Juan", "San Luis", "Santa Cruz", "Santa Fe", "Santiago del Estero", "Tierra del Fuego", "Tucumán"]
    
    # Obtener credenciales y detalles de la base de datos Redshift desde las variables de entorno
    dbname = os.getenv('REDSHIFT_DBNAME')
    user = os.getenv('REDSHIFT_USERNAME')
    password = os.getenv('REDSHIFT_PASSWORD')
    host = os.getenv('REDSHIFT_HOST')
    port = os.getenv('REDSHIFT_PORT')
    
    # Conectar a la base de datos Redshift
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    
    # Ejecutar el script SQL para crear tablas en Redshift
    run_sql_file("create_table.sql", conn)
    
    # Ejecutar el proceso ETL
    run_etl(api_key, provinces, conn)
    
    # Cerrar la conexión a la base de datos
    conn.close()