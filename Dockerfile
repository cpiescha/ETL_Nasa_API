# Usar la imagen base de Airflow
FROM apache/airflow:2.10.2

# Establecer el directorio de trabajo
WORKDIR /opt/airflow

# Instalar librerías adicionales
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN airflow db init

# Establecer el comando para ejecutar el scheduler y webserver
CMD ["sh", "-c", "airflow scheduler & airflow webserver --port 8080"]