import os
from dotenv import load_dotenv

class Config:
    load_dotenv()

    # COSMOS_DB_URI = os.getenv('COSMOS_DB_URI')
    # COSMOS_DB_KEY = os.getenv('COSMOS_DB_KEY')
    # COSMOS_DB_DATABASE_NAME = os.getenv('COSMOS_DB_DATABASE_NAME')

    MONGO_DB_URI = os.getenv('MONGO_DB_URI')
    MONGO_DB_NAME = os.getenv('MONGO_DB_NAME')
