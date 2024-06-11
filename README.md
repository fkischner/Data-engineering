# Proyecto ETL para Datos Climáticos

Este proyecto implementa un pipeline ETL (Extract, Transform, Load) para obtener datos climáticos de la API de OpenWeatherMap, transformarlos y cargarlos en una base de datos Redshift para su análisis y visualización.

## Descripción

El objetivo de este proyecto es automatizar el proceso de obtención, transformación y carga de datos climáticos en Redshift. Este pipeline ETL obtiene los datos climáticos actuales para una ciudad específica, los transforma en un formato adecuado y los carga en una tabla en Redshift.

## Instalación

### Requisitos Previos

- Python 3.6 o superior
- pip (Python package installer)

### Pasos de Instalación

1. Clona este repositorio:
    ```bash
    git clone https://github.com/fkischner/fkischner-prueba.git
    cd fkischner-prueba
    ```

2. Instala las dependencias necesarias:
    ```bash
    pip install -r requirements.txt
    ```

## Configuración

Crea un archivo `.env` en el directorio raíz del proyecto con las siguientes variables de entorno. Esto es necesario para configurar la conexión a tu base de datos Redshift: