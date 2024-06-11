import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

def load_data_to_redshift(df):
    # Verificar el contenido del DataFrame
    print("Contenido del DataFrame a cargar:")
    print(df)

    engine = create_engine(
        'postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}'.format(
            user=os.getenv('REDSHIFT_USERNAME'),
            password=os.getenv('REDSHIFT_PASSWORD'),
            host=os.getenv('REDSHIFT_HOST'),
            port=os.getenv('REDSHIFT_PORT'),
            dbname=os.getenv('REDSHIFT_DBNAME')
        )
    )
    try:
        df.to_sql('weather_data', con=engine, schema='federicokischner_coderhouse', if_exists='append', index=False)
        print("Datos cargados exitosamente en Redshift")
        return True
    except Exception as e:
        print(f"No se pudo cargar los datos en Redshift: {e}")
        return False