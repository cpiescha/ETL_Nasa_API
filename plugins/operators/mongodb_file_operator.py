from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from pymongo import MongoClient
import json
import time

class MongoDBOperator(BaseOperator):
    
    
    @apply_defaults
    def __init__(self, mongo_conn_id: str, database: str, collection: str, operation: str,json_file_path=None, data=None, query=None, **kwargs):
        
            
        super().__init__(**kwargs)
        self.mongo_conn_id = mongo_conn_id
        self.database = database
        self.json_file_path = json_file_path
        self.collection = collection
        self.operation = operation
        self.data = data or {}
        self.query = query or {}

    def execute(self, context):
        from airflow.hooks.base import BaseHook
        if self.json_file_path:
            try:
                with open(self.json_file_path, 'r') as file:
                    self.data = json.load(file)
            except FileNotFoundError:
                self.log.error(f"JSON file not found: {self.json_file_path}")
                raise

        # Obtener la conexión configurada en Airflow
        connection = BaseHook.get_connection(self.mongo_conn_id)
        client = MongoClient(
            host=connection.host,
            port=connection.port,
            username=connection.login,
            password=connection.password
        )

        db = client[self.database]
        collection = db[self.collection]

        # Ejecutar operación según lo especificado
        if self.operation == 'insert':
            if isinstance(self.data, list):
                for doc in self.data:
                    if isinstance(doc, dict):
                        result = collection.insert_one(doc)
                        self.log.info(f"Inserted document ID: {result.inserted_id}")
                    else:
                        self.log.warning(f"Skipped non-dictionary item: {doc}")
            elif isinstance(self.data, dict):
                result = collection.insert_one(self.data)
                self.log.info(f"Inserted document ID: {result.inserted_id}")
            else:
                raise TypeError("Data must be a dictionary or a list of dictionaries.")
        elif self.operation == 'find':
            result = list(collection.find(self.query))
            self.log.info(f"Found documents: {result}")
            return result
        elif self.operation == 'update':
            result = collection.update_many(self.query, self.data)
            self.log.info(f"Updated {result.modified_count} documents")
        elif self.operation == 'delete':
            result = collection.delete_many(self.query)
            self.log.info(f"Deleted {result.deleted_count} documents")
        else:
            raise ValueError(f"Unsupported operation: {self.operation}")

        client.close()