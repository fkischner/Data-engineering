-- create_table.sql
CREATE TABLE IF NOT EXISTS weather_data (
    city VARCHAR(255),
    temperature FLOAT,
    humidity INTEGER,
    pressure INTEGER,
    weather VARCHAR(255),
    wind_speed FLOAT,
    timestamp TIMESTAMP
);
