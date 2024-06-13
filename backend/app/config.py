import os
from dotenv import load_dotenv

class Config:
    load_dotenv()

    MONGO_DB_URI = os.getenv('MONGO_DB_URI')
    MONGO_DB_NAME = os.getenv('MONGO_DB_NAME')