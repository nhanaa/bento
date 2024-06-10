from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from pymongo.errors import DuplicateKeyError

from .custom_vectorstore import CustomAzureCosmosDBVectorSearch
from ..app import db
from ..utils.ai_tools import huggingface_embeddings

"""
For ONE given website url, document id, and document summary, create and add chunks to vector db
user id, folder_id
"""


class Chunk:
    CHUNK_COLLECTION_NAME = "chunks"
    embedding_key = "vectorContent"

    def __init__(self):
        self.chunk_collection = db[self.CHUNK_COLLECTION_NAME]
        self.chunk_vectorstore = CustomAzureCosmosDBVectorSearch(
            self.chunk_collection,
            huggingface_embeddings,
            embedding_key=self.embedding_key,
        )
        self.ensure_indexes()

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
        existing_indexes = self.chunk_collection.list_indexes()
        existing_index_names = [index["name"] for index in existing_indexes]

        for index_def in index_definitions:
            index_name = index_def["name"]
            if index_name not in existing_index_names:
                try:
                    db.command(
                        {
                            "createIndexes": self.CHUNK_COLLECTION_NAME,
                            "indexes": [index_def],
                        }
                    )
                    print(f"Index '{index_name}' created successfully.")
                except DuplicateKeyError as e:
                    print(f"Error creating index '{index_name}': {e}")
            else:
                print(f"Index '{index_name}' already exists.")

    async def create_chunks(
        self, user_id: str, folder_id: str, document_id: str, url: str, doc_summary: str
    ):
        loader = WebBaseLoader(
            web_path=url,
            verify_ssl=False,
            bs_get_text_kwargs={"strip": True, "separator": " "},
        )
        document_list = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
        docs = text_splitter.split_documents(document_list)

        # Add metadata to the documents
        for doc in docs:
            doc.page_content += doc_summary
            doc.metadata.update(
                {"user_id": user_id, "folder_id": folder_id, "document_id": document_id}
            )

        # Add the documents to the vector store
        await self.chunk_vectorstore.aadd_documents(docs)
