# Usar la imagen base de Airflow
FROM apache/airflow:2.10.2

# Establecer el directorio de trabajo
WORKDIR /opt/airflow

# Instalar librerías adicionales
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
