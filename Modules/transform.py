import pandas as pd

def transform_data(weather_data):
    data_list = []
    for province, data in weather_data.items():
        if data:
            entry = {
                'province': province,
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'weather': data['weather'][0]['description'],
                'wind_speed': data['wind']['speed'],
                'timestamp': pd.Timestamp.now()
            }
            data_list.append(entry)
    df = pd.DataFrame(data_list)
    
    # Eliminar filas con datos nulos
    df.dropna(inplace=True)
    
    print("Contenido del DataFrame transformado (sin nulos):")
    print(df)
    return df