from azure.core.exceptions import AzureError
from azure.cosmos import CosmosClient, PartitionKey

class CosmosDB:
    client = None
    database = None
    containers = {}

    @classmethod
    def init_app(cls, app):
        cls.client = CosmosClient(app.config['COSMOS_DB_URI'], credential=app.config['COSMOS_DB_KEY'])
        cls.database = cls.client.create_database_if_not_exists(id=app.config['COSMOS_DB_DATABASE_NAME'])
        cls.create_containers()

        return (cls, app)

    @classmethod
    def create_containers(cls):
        cls.containers['Users'] = cls.database.create_container_if_not_exists(
            id='Users',
            partition_key=PartitionKey(path='/id')
        )
        cls.containers['Folders'] = cls.database.create_container_if_not_exists(
            id='Folders',
            partition_key=PartitionKey(path='/id')
        )
        cls.containers['Files'] = cls.database.create_container_if_not_exists(
            id='Files',
            partition_key=PartitionKey(path='/id')
        )

    @classmethod
    def get_container(cls, container_name):
        return cls.containers.get(container_name)
