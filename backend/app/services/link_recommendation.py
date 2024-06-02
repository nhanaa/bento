from datetime import datetime
from typing import List, Union, Any

import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, HttpUrl, field_serializer
from typing_extensions import Annotated
from langchain_community.document_loaders import WebBaseLoader
from custom_vectorstore import CustomAzureCosmosDBVectorSearch
from langchain_community.vectorstores.azure_cosmos_db import AzureCosmosDBVectorSearch
from langchain_openai import AzureChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

# from motor.motor_asyncio import AsyncIOMotorClient


# Load environment variables from a .env file
load_dotenv()

# Initialize FastAPI application
app = FastAPI()

# Set up connection details
CONNECTION_STRING = os.getenv("AZURE_COSMOS_DB_CONNECTION_STRING")
DB_NAME = "bento"

# Initialize MongoDB client
mongo_client = MongoClient(CONNECTION_STRING)
db = mongo_client[DB_NAME]

# Initialize the embedding model
model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": False}
huggingface_embeddings = HuggingFaceEmbeddings(
    model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
)


# Exception handling for HTTP exceptions
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


# Exception handling for request validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


# Define the data models
class VisitData(BaseModel):
    id: int
    lastVisitTime: datetime
    title: str
    typedCount: int
    url: HttpUrl  # this is used to eliminate possible replication of 2 urls leading to the same page
    visitCount: int


class LinkRecInput(BaseModel):
    query: str


# Define the API endpoint for getting link recommendations
@app.get("/get_links/{user_id}")
def get_links(user_id: str, req_body: LinkRecInput = Body(...)) -> List[str]:
    """
    This assumes that the browsing history is stored in the Azure Cosmos DB
    and its title and URL are combined, embedded, and stored as vectors.
    For example:
    title = "Hello world"
    url = "https://example.com"
    combined_title_url = title + " " + url -> "Hello world https://example.com"
    """
    try:
        COLLECTION_NAME = "browsing_history"
        collection = db[COLLECTION_NAME]

        # Initialize the vector store
        vectorstore = AzureCosmosDBVectorSearch(
            collection=collection,
            embedding=huggingface_embeddings,
            index_name="website_vector_index",
            embedding_key="website_vector_field",
            # look for the url to return as page content, the rest will be considered metadata
            text_key="url",
        )
        if not vectorstore.index_exists():
            vectorstore.create_index(dimensions=768)

        # Perform similarity search
        similar_documents = vectorstore.similarity_search(
            req_body.query, score_threshold=0.35, k=10
        )

        # Return the search results
        return [doc.page_content for doc in similar_documents]

    except Exception as e:
        # Handle potential errors
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/create_chunks/{user_id}/{folder_id}", status_code=201)
def create_chunks(
    user_id: str, folder_id: str, links_list: List[HttpUrl] = Body(...)
) -> str:
    try:
        COLLECTION_NAME = "documents"
        collection = db[COLLECTION_NAME]
        embedding_key = "vectorContent"

        # Initialize the vector store
        vectorstore = CustomAzureCosmosDBVectorSearch(
            collection,
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
        ensure_index(collection, index_definitions, COLLECTION_NAME)

        # Load documents from the web links
        loader = WebBaseLoader(
            web_paths=[str(link) for link in links_list],
            verify_ssl=False,
            bs_get_text_kwargs={"strip": True, "separator": " "},
        )
        document_list = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
        docs = text_splitter.split_documents(document_list)

        # Add metadata to the documents
        for doc in docs:
            doc.metadata.update({"user_id": user_id, "folder_id": folder_id})

        # Add the documents to the vector store
        vectorstore.add_documents(docs)

        return "Folder created successfully."
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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


@app.post("/insert_browsing_history", status_code=201)
def insert_browsing_history(data: List[VisitData] = Body(...)) -> None:
    """
    Inserts the browsing history data into the Azure Cosmos DB.
    """
    try:
        COLLECTION_NAME = "browsing_history"
        collection = db.get_collection(COLLECTION_NAME)

        # Insert the data into the collection
        for item in data:
            my_dict = item.model_dump()
            url_in_str = str(my_dict["url"])
            my_str = my_dict["title"] + " " + url_in_str
            my_dict["url"] = url_in_str
            my_dict["website_vector_field"] = huggingface_embeddings.embed_query(my_str)
            collection.insert_one(my_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
