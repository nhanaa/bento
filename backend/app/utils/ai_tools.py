from langchain_openai import AzureChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import certifi
from ..services.custom_vectorstore import CustomAzureCosmosDBVectorSearch

load_dotenv()

CONNECTION_STRING = os.getenv("AZURE_COSMOS_DB_CONNECTION_STRING")
DB_NAME = "bento"
mongo_client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())
db = mongo_client[DB_NAME]

llm = AzureChatOpenAI(
    temperature=0,
    model_name="gpt-4-32k",
    openai_api_version="2024-02-01",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)

model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": False}
huggingface_embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs,
    show_progress=True,
)



"""
Experimenting. THIS IS THE SECTION FOR CHUNKS
"""
embedding_key = "vectorContent"
CHUNK_COLLECTION_NAME = "chunks"
chunk_collection = db[CHUNK_COLLECTION_NAME]
chunk_vectorstore = CustomAzureCosmosDBVectorSearch(
    chunk_collection,
    huggingface_embeddings,
    embedding_key=embedding_key,
)

# ensure indices
index_definitions = [
    # add index for user_id and folder_id (metadata)
    {"key": {"user_id": 1}, "name": "user_filter"},
    {"key": {"folder_id": 1}, "name": "folder_filter"},
    # add index for vector content (for vector search)
    {
        "name": "TitleVectorSearchIndex",
        "key": {embedding_key: "cosmosSearch"},
        "cosmosSearchOptions": {
            "kind": "vector-ivf",
            "numLists": 1,
            "similarity": "COS",
            "dimensions": 768,
        },
    },
]


def ensure_index(collection, index_definitions, collection_name: str):
    """
    Ensures that the specified indexes exist on the collection.
    If they don't exist, it creates the indexes.
    """
    # Check existing indexes
    existing_indexes = collection.list_indexes()
    existing_index_names = [index["name"] for index in existing_indexes]

    for index_def in index_definitions:
        index_name = index_def["name"]
        if index_name not in existing_index_names:
            try:
                db.command({"createIndexes": collection_name, "indexes": [index_def]})
                print(f"Index '{index_name}' created successfully.")
            except DuplicateKeyError as e:
                print(f"Error creating index '{index_name}': {e}")
        else:
            print(f"Index '{index_name}' already exists.")


ensure_index(chunk_collection, index_definitions, CHUNK_COLLECTION_NAME)
