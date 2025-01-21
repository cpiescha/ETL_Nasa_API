from datetime import timedelta,datetime
# The DAG object; we'll need this to instantiate a DAG
from airflow.models import DAG
#from airflow.operators.python import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from airflow.providers.mongo.hooks.mongo import MongoHook
from operators.mongodb_file_operator import MongoDBOperator
from airflow.operators.python import PythonOperator
# from operators import PostgresFileOperator

#defining DAG arguments
# You can override them on a per-task basis during operator initialization

    
    
default_args = {
     'owner': 'camilo',
     'start_date': days_ago(0),
     'email': ['milo0@gmail.com'],
     'email_on_failure': False,
     'email_on_retry': False,
     'retries': 1,
     'retry_delay': timedelta(minutes=5),
 }


def create_database_and_collection(mongo_conn_id, database_name, collection_name):
    # Conexión a MongoDB usando MongoHook
    hook = MongoHook(mongo_conn_id=mongo_conn_id)
    client = hook.get_conn()

    # Verificar si la colección existe
    db = client[database_name]
    if collection_name not in db.list_collection_names():
        # Crear colección insertando un documento inicial
        db[collection_name].insert_one({"message": "Initial document"})
        print(f"Collection '{collection_name}' created in database '{database_name}'.")
    else:
        print(f"Collection '{collection_name}' already exists in database '{database_name}'.")
 # defining the DAG
 # define the DAG
dag = DAG(
     dag_id='nasa_dag',
     default_args=default_args,
     schedule_interval='@hourly',
     catchup=False,
     max_active_runs=1,
     concurrency=1
 )

extract_data = BashOperator(
    task_id='extract_data',
    bash_command='python /opt/airflow/tmp/extract_api_nasa.py',
    dag=dag
)

create_database_task = PythonOperator(
        task_id='create_database_and_collection',
        python_callable=create_database_and_collection,
        op_kwargs={
            'mongo_conn_id': 'mongo_default',
            'database_name': 'etl_nasa',
            'collection_name': 'nasa_images'
        }
    )

insert_data = MongoDBOperator(
        task_id='insert_data',
        mongo_conn_id='mongo_default',
        database='etl_nasa',
        collection='etl_nasa',
        operation='insert',
        data={'key': 'value'},
    )
 

extract_data