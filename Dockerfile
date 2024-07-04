# Usar una imagen base de Python
FROM python:3.9

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos de requerimientos y el archivo .env al contenedor
COPY requirements.txt requirements.txt
COPY .env .env

# Instalar las dependencias del archivo requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación al contenedor
COPY . .

# Comando por defecto para ejecutar el script principal
CMD ["python", "main.py"]