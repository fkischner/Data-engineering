import requests
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener la clave API desde las variables de entorno
API_KEY = os.getenv('OPENWEATHER_API_KEY')

def fetch_data_from_api(api_key, provinces):
    weather_data = {}
    for province in provinces:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={province},AR&appid={api_key}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            weather_data[province] = response.json()
            print(f"{province} -> Datos extraidos correctamente")
        else:
            print(f"{province} -> Error en la extracción: ({response.status_code})")
    return weather_data

# Ejemplo de cómo utilizar este módulo si se ejecuta como script principal
if __name__ == "__main__":
    provinces = [
        "Buenos Aires", "Catamarca", "Chaco", "Chubut", "Córdoba",
        "Corrientes", "Entre Ríos", "Formosa", "Jujuy", "La Pampa",
        "La Rioja", "Mendoza", "Misiones", "Neuquén", "Río Negro",
        "Salta", "San Juan", "San Luis", "Santa Cruz", "Santa Fe",
        "Santiago del Estero", "Tierra del Fuego", "Tucumán"
    ]
    weather_data = fetch_data_from_api(provinces)