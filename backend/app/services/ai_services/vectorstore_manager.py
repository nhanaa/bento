from pymongo.errors import DuplicateKeyError
from .custom_vectorstore import CustomAzureCosmosDBVectorSearch
from app import db
from utils.ai_tools import huggingface_embeddings

class VectorStoreManager:
    def __init__(self, collection, embedding_key):
        self.collection = collection
        self.embedding_key = embedding_key
        self.vectorstore = CustomAzureCosmosDBVectorSearch(
            collection,
            huggingface_embeddings,
            embedding_key=embedding_key,
        )
        self.ensure_indexes()

    def get_vectorstore(self):
        return self.vectorstore

    def get_retriever(self, user_id, folder_id):
        return self.vectorstore.as_retriever(
            search_kwargs={
                "pre_filter": {"user_id": user_id, "folder_id": folder_id},
                "k": 5,
                "score_threshold": 0.5,
            }
        )

    def ensure_indexes(self):
        index_definitions = [
            {"key": {"user_id": 1}, "name": "user_filter"},
            {"key": {"folder_id": 1}, "name": "folder_filter"},
            {
                "name": "TitleVectorSearchIndex",
                "key": {self.embedding_key: "cosmosSearch"},
                "cosmosSearchOptions": {
                    "kind": "vector-ivf",
                    "numLists": 1,
                    "similarity": "COS",
                    "dimensions": 768,
                },
            },
        ]
        existing_indexes = self.collection.list_indexes()
        existing_index_names = [index["name"] for index in existing_indexes]

        for index_def in index_definitions:
            index_name = index_def["name"]
            if index_name not in existing_index_names:
                try:
                    db.command(
                        {
                            "createIndexes": self.collection.name,
                            "indexes": [index_def],
                        }
                    )
                    print(f"Index '{index_name}' created successfully.")
                except DuplicateKeyError as e:
                    print(f"Error creating index '{index_name}': {e}")
            else:
                print(f"Index '{index_name}' already exists.")
