from uuid import UUID
from datetime import datetime
from typing import List, Union

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, HttpUrl
from typing_extensions import Annotated

from langchain_community.vectorstores.azure_cosmos_db import (
    AzureCosmosDBVectorSearch,
    CosmosDBSimilarityType,
    CosmosDBVectorSearchType,
)
from langchain_openai import AzureChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings

# Load environment variables from a .env file
load_dotenv()

# Initialize FastAPI application
app = FastAPI()

# Set up connection details
CONNECTION_STRING = os.getenv("AZURE_COSMOS_DB_CONNECTION_STRING")
NAMESPACE = "bento.browsing_history"
DB_NAME, COLLECTION_NAME = NAMESPACE.split(".")

# Initialize MongoDB client
mongo_client = MongoClient(CONNECTION_STRING)
db = mongo_client[DB_NAME]
collection = db[COLLECTION_NAME]

# Initialize the embedding model
model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": False}
huggingface_embeddings = HuggingFaceEmbeddings(
    model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
)

# Initialize the vector store
vectorstore = AzureCosmosDBVectorSearch(
    collection,
    huggingface_embeddings,
    index_name="website_vector_index",
    embedding_key="website_vector_field",
)

# Ensure the index is created if not already
if not vectorstore.is_indexed():
    vectorstore.create_index(num_lists=1, dimensions=768)


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
    id: UUID
    lastVisitTime: float
    title: str
    typedCount: int
    url: HttpUrl
    visitCount: int


class LinkRecommendation(BaseModel):
    title: str
    url: HttpUrl


# Define the API endpoint for getting link recommendations
@app.get("/get_links/{user_id}")
def get_links(query: str) -> List[LinkRecommendation]:
    """
    This assumes that the browsing history is stored in the Azure Cosmos DB
    and its title and URL are combined, embedded, and stored as vectors.
    This also assumes that the vector is indexed and is ready to be searched.
    For example:
    title = "Hello world"
    url = "https://example.com"
    combined_title_url = title + " " + url -> "Hello world https://example.com"
    """
    try:
        # Encode the query using the embedding model
        query_vector = huggingface_embeddings.encode(query)

        # Perform similarity search
        similar_vectors: List[VisitData] = vectorstore.similarity_search(
            query_vector, k=10, score_threshold=0.5
        )

        # Return the search results
        return [
            LinkRecommendation(title=vector.title, url=vector.url)
            for vector in similar_vectors
        ]
    except Exception as e:
        # Handle potential errors
        raise HTTPException(status_code=500, detail=str(e))
