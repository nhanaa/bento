from datetime import datetime
from typing import List, Union, Any, Dict

import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, HttpUrl, field_serializer
from typing_extensions import Annotated
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores.azure_cosmos_db import AzureCosmosDBVectorSearch
from langchain_openai import AzureChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import certifi


# from motor.motor_asyncio import AsyncIOMotorClient


# Load environment variables from a .env file
load_dotenv()

# Initialize FastAPI application
app = FastAPI()

# Set up connection details
CONNECTION_STRING = os.getenv("AZURE_COSMOS_DB_CONNECTION_STRING")
DB_NAME = "bento"

# Initialize MongoDB client
mongo_client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())
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
    url: HttpUrl
    visitCount: int


# return a json format of list of urls
def get_links(user_id: str, desc: str) -> Dict[str, List[str]]:
    """
    This assumes that the browsing history is stored in the Azure Cosmos DB
    and its title and URL are combined, embedded, and stored as vectors.
    For example:
    title = "Hello world"
    url = "https://example.com"
    combined_title_url = title + " " + url -> "Hello world https://example.com"
    """
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
    similar_documents = vectorstore.similarity_search(desc, score_threshold=0.35, k=10)

    # Return the search results
    return {"links_list": [doc.page_content for doc in similar_documents]}


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


@app.get("/test")
def test_endpoint():
    return {"message": "This is a test"}
