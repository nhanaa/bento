from pymongo.errors import DuplicateKeyError
from utils.custom_vectorstore import CustomAzureCosmosDBVectorSearch
from typing import Dict
from app import db
from utils.ai_tools import huggingface_embeddings


class VectorStoreWithFilter:

    def __init__(self, collection_name, embedding_key, **kwargs):
        """
        Initializes the YourClass object.

        Parameters:
        collection_name: The collection to be used.
        embedding_key: The embedding key.
        filter_index_defs: Optional; can be either a single dictionary or a list of dictionaries.
                        Example list of dictionaries:
                        [
                            {"key": {"user_id": 1}, "name": "user_filter"},
                            {"key": {"folder_id": 1}, "name": "folder_filter"},
                        ]
        text_key: key that langchain will return as result of vector similarity search 
        """
        if collection_name not in db.list_collection_names():
            db.create_collection(collection_name)
        self.collection = db[collection_name]
        self.embedding_key = embedding_key
        self.vectorstore = CustomAzureCosmosDBVectorSearch(
            self.collection,
            huggingface_embeddings,
            embedding_key=embedding_key,
            text_key=kwargs.get("text_key", "textContent"),
        )
        if not self.vectorstore.index_exists():
            self.vectorstore.create_index(dimensions=768)
        filter_index_defs = kwargs.get("filter_index_defs", None)
        if filter_index_defs:
            self.index_definitions = filter_index_defs
            self.ensure_filter_indexes()

    def get_vectorstore(self):
        return self.vectorstore

    def get_retriever(self, filter_dict: Dict[str, str]):
        return self.vectorstore.as_retriever(
            search_kwargs={
                "pre_filter": filter_dict,
                "k": 5,
                "score_threshold": 0.5,
            }
        )

    def search_similarity(self, query: str, filter_dict: Dict[str, str]):
        return self.vectorstore.similarity_search(
            query, score_threshold=0.35, k=6, pre_filter=filter_dict
        )

    def ensure_filter_indexes(self):
        existing_indexes = self.collection.list_indexes()
        existing_index_names = [index["name"] for index in existing_indexes]

        for index_def in self.index_definitions:
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
