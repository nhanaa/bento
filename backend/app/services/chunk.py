from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import os
import certifi
from langchain_community.document_loaders import WebBaseLoader
from .custom_vectorstore import CustomAzureCosmosDBVectorSearch
from ..utils.ai_tools import chunk_vectorstore

# CONNECTION_STRING = os.getenv("AZURE_COSMOS_DB_CONNECTION_STRING")
# DB_NAME = "bento"

# # Initialize MongoDB client
# mongo_client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())
# db = mongo_client[DB_NAME]


"""
For ONE given website url, document id, and document summary, create and add chunks to vector db
user id, folder_id
"""


async def create_chunks(
    user_id: str, folder_id: str, document_id: str, url: str, doc_summary: str
):
    # COLLECTION_NAME = "chunks"
    # collection = db[COLLECTION_NAME]
    # embedding_key = "vectorContent"

    # # Initialize the vector store
    # vectorstore = CustomAzureCosmosDBVectorSearch(
    #     collection,
    #     huggingface_embeddings,
    #     embedding_key=embedding_key,
    # )

    # # ensure indices
    # index_definitions = [
    #     # add index for user_id and folder_id (metadata)
    #     {"key": {"user_id": 1}, "name": "user_filter"},
    #     {"key": {"folder_id": 1}, "name": "folder_filter"},
    #     # add index for vector content (for vector search)
    #     {
    #         "name": "TitleVectorSearchIndex",
    #         "key": {embedding_key: "cosmosSearch"},
    #         "cosmosSearchOptions": {
    #             "kind": "vector-ivf",
    #             "numLists": 1,
    #             "similarity": "COS",
    #             "dimensions": 768,
    #         },
    #     },
    # ]
    # ensure_index(collection, index_definitions, COLLECTION_NAME)
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
    await chunk_vectorstore.aadd_documents(docs)


# def ensure_index(collection, index_definitions, collection_name: str):
#     """
#     Ensures that the specified indexes exist on the collection.
#     If they don't exist, it creates the indexes.
#     """
#     # Check existing indexes
#     existing_indexes = collection.list_indexes()
#     existing_index_names = [index["name"] for index in existing_indexes]

#     for index_def in index_definitions:
#         index_name = index_def["name"]
#         if index_name not in existing_index_names:
#             try:
#                 db.command({"createIndexes": collection_name, "indexes": [index_def]})
#                 print(f"Index '{index_name}' created successfully.")
#             except DuplicateKeyError as e:
#                 print(f"Error creating index '{index_name}': {e}")
#         else:
#             print(f"Index '{index_name}' already exists.")
