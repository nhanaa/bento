from pymongo import MongoClient
import certifi
import os
from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime
from .summarization import summarize_pdf
from .chunk import create_chunks
from ..models.rag_model import Document
from motor.motor_asyncio import AsyncIOMotorClient


CONNECTION_STRING = os.getenv("AZURE_COSMOS_DB_CONNECTION_STRING")
DB_NAME = "bento"

# Initialize MongoDB client
# mongo_client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())
# db = mongo_client[DB_NAME]
mongo_client = AsyncIOMotorClient(CONNECTION_STRING, tlsCAFile=certifi.where())
db = mongo_client.bento


async def insert_document_to_db(document_data: dict) -> str:
    collection_name = "documents"
    # collection = db[collection_name]
    collection = db.get_collection(collection_name)
    result = await collection.insert_one(document_data)

    # Return the ID of the inserted document
    return str(result.inserted_id)


"""
    This function performs the following operations:
    1. Calls `summarize_pdf` to get a summary of the document at the specified URL.
    2. Extracts the summary from the result and prepares the document data.
    3. Inserts the document data into the database and retrieves the document ID.
    4. Calls `create_chunks` to split the document into manageable chunks and stores them in the database.
"""


async def process_one_document(user_id: str, folder_id: str, url: str):
    res = await summarize_pdf(url)
    print(f"Received summary data: {res}")
    summary = res.get("summary", "")
    doc = Document(**res).model_dump()
    document_id = await insert_document_to_db(doc)
    print(f"Document inserted with ID: {document_id}")
    await create_chunks(user_id, folder_id, document_id, url, summary)
    print("Document processing complete.")
