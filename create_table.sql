-- Crear la tabla principal si no existe
CREATE TABLE IF NOT EXISTS weather_data (
    province VARCHAR(255),
    temperature FLOAT,
    humidity INTEGER,
    pressure INTEGER,
    weather VARCHAR(255),
    wind_speed FLOAT,
    timestamp TIMESTAMP,
    PRIMARY KEY (province)  -- Estableciendo 'province' como clave primaria
);

-- Crear la tabla temporal si no existe
CREATE TEMP TABLE IF NOT EXISTS temp_weather_data (LIKE weather_data);