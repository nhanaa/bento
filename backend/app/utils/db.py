from pymongo import MongoClient

class MongoDB:
    client = None
    db = None
    collections = {}

    @classmethod
    def init_app(cls, app):
        cls.client = MongoClient(app.config['MONGO_DB_URI'])
        cls.db = cls.client[app.config['MONGO_DB_NAME']]
        cls.collections['Users'] = cls.db['Users']
        cls.collections['Folders'] = cls.db['Folders']
    
    @classmethod
    def get_collection(cls, collection_name):
        return cls.collections.get(collection_name)
