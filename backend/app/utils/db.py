import certifi
from pymongo import MongoClient, errors

class MongoDB:
    client = None
    db = None
    collections = {}

    @classmethod
    def init_app(cls, app):
        try:
            cls.client = MongoClient(app.config['MONGO_DB_URI'], tlsCAFile=certifi.where())
            cls.db = cls.client[app.config['MONGO_DB_NAME']]
            cls.collections['users'] = cls.db['users']
            cls.collections['folders'] = cls.db['folders']
            info = cls.client.server_info()
            print("Mongo connection is ready", info)
        except errors.ServerSelectionTimeoutError as err:
            print("Mongo initalize failed", err)

    @classmethod
    def get_collection(cls, collection_name):
        return cls.collections.get(collection_name)
