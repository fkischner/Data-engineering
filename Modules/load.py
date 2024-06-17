import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

def load_data_to_redshift(df, conn):
    print("Contenido del DataFrame a cargar:")
    print(df)

    cursor = conn.cursor()

    # Crear tabla temporal si no existe (opcional aquí, dependiendo de la configuración inicial)
    cursor.execute("""
    CREATE TEMP TABLE IF NOT EXISTS temp_weather_data (LIKE weather_data);
    """)

    # Preparar los datos para la inserción SQL
    insert_query = 'INSERT INTO temp_weather_data (province, temperature, humidity, pressure, weather, wind_speed, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s)'

    # Insertar datos en la tabla temporal
    try:
        for _, row in df.iterrows():
            cursor.execute(insert_query, tuple(row))
        conn.commit()
        print("Datos cargados exitosamente en la tabla temporal de Redshift")
    except Exception as e:
        print(f"No se pudo cargar los datos en la tabla temporal de Redshift: {e}")
        conn.rollback()
        return False

    # Sincronizar datos desde la tabla temporal a la principal
    try:
        cursor.execute("""
        BEGIN;

        -- Elimina registros que coincidan en la tabla principal
        DELETE FROM weather_data
        USING temp_weather_data
        WHERE weather_data.province = temp_weather_data.province;

        -- Inserta los nuevos datos desde la tabla temporal
        INSERT INTO weather_data
        SELECT * FROM temp_weather_data;

        TRUNCATE TABLE temp_weather_data;

        COMMIT;
        """)
        conn.commit()
        print("Sincronización completada exitosamente en Redshift")
        return True
    except Exception as e:
        print(f"Error durante la sincronización en Redshift: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
