
import pandas as pd

def transform_data(data):
    df = pd.DataFrame([{
        'city': data['name'],
        'temperature': data['main']['temp'],
        'humidity': data['main']['humidity'],
        'pressure': data['main']['pressure'],
        'weather': data['weather'][0]['description'],
        'wind_speed': data['wind']['speed'],
        'timestamp': pd.Timestamp.now()
    }])

    # Verificar el contenido del DataFrame transformado
    print("Contenido del DataFrame transformado:")
    print(df)
    
    return df
