import os
from dotenv import load_dotenv

class Config:
    load_dotenv()

    COSMOS_DB_URI = os.getenv('COSMOS_DB_URI')
    COSMOS_DB_KEY = os.getenv('COSMOS_DB_KEY')
    COSMOS_DB_DATABASE_NAME = os.getenv('COSMOS_DB_DATABASE_NAME')
    # COSMOS_CONTAINER_NAME = os.getenv('COSMOS_CONTAINER_NAME', 'Users')

    print(222, os.getenv('COSMOS_DB_URI'))
