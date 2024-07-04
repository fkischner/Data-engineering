FROM python:3.9

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de requisitos al contenedor de trabajo
COPY requirements.txt requirements.txt

# Instalar dependencias del sistema necesarias
RUN apt-get update && \
    apt-get install -y gcc libpq-dev

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos de la aplicación al contenedor de trabajo
COPY . .

# Comando para ejecutar tu aplicación
CMD ["python", "main.py"]