from azure.core.exceptions import AzureError
from azure.cosmos import CosmosClient, PartitionKey

class CosmosDB:
    client = None
    database = None
    containers = {}

    @classmethod
    def init_app(cls, config):
        print(config.COSMOS_DB_URI)
        cls.client = CosmosClient(config.COSMOS_DB_URI, credential=config.COSMOS_DB_KEY)
        cls.database = cls.client.create_database_if_not_exists(id=config.COSMOS_DB_DATABASE_NAME)
        cls.create_containers()

    @classmethod
    def create_collection(cls):
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
