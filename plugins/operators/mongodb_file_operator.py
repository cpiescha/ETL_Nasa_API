from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from pymongo import MongoClient

class MongoDBOperator(BaseOperator):
    @apply_defaults
    def __init__(self, mongo_conn_id: str, database: str, collection: str, operation: str, data=None, query=None, **kwargs):
        super().__init__(**kwargs)
        self.mongo_conn_id = mongo_conn_id
        self.database = database
        self.collection = collection
        self.operation = operation
        self.data = data or {}
        self.query = query or {}

    def execute(self, context):
        from airflow.hooks.base import BaseHook

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
            result = collection.insert_many(self.data if isinstance(self.data, list) else [self.data])
            self.log.info(f"Inserted documents: {result.inserted_ids}")
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