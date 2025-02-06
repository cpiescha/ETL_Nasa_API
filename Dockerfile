FROM apache/airflow:2.10.2

# Crear carpetas dentro del contenedor
USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev && \
    rm -rf /var/lib/apt/lists/*


RUN mkdir -p /opt/airflow/img && \
    mkdir -p /opt/airflow/tmp && \
    chown -R airflow:0 /opt/airflow/img /opt/airflow/tmp  # Permisos para el usuario airflow

# Configuración de Airflow
ENV AIRFLOW_HOME=/opt/airflow
ENV AIRFLOW__CORE__EXECUTOR=LocalExecutor
ENV AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION='false'
ENV AIRFLOW__CORE__LOAD_EXAMPLES='false'
ENV AIRFLOW__DATABASE__SQL_ALCHEMY_CONN = postgresql+psycopg2://postgres:wOCWPTrwqRsmyaoQOuKLwVmUwPfVpocB@postgres.railway.internal:5432/railway




# Instalar dependencias (ejemplo)
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copiar DAGs, plugins y configuraciones
COPY ./dags/ ${AIRFLOW_HOME}/dags/
COPY ./plugins/ ${AIRFLOW_HOME}/plugins/

# Volver al usuario airflow
USER airflow
RUN pip install --upgrade pip && pip install psycopg2-binary

# Comando de inicio
CMD airflow db init && \
    airflow users create \
    --username admin \
    --password admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com && \
    (airflow scheduler & airflow webserver --port 8080)