from pymongo import MongoClient
import certifi
import os
from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime
from .summarization import summarize_pdf
from .chunk import create_chunks

CONNECTION_STRING = os.getenv("AZURE_COSMOS_DB_CONNECTION_STRING")
DB_NAME = "bento"

# Initialize MongoDB client
mongo_client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())
db = mongo_client[DB_NAME]


class Document(BaseModel):
    title: str = Field(
        ..., title="Document Title", description="The title of the document"
    )
    summary: str = Field(
        ..., title="Summary", description="A brief summary of the document"
    )
    created_date: datetime = Field(
        default_factory=datetime.now,
        title="Creation Date",
        description="The date and time the document was created",
    )


def insert_document_to_db(document_data: dict) -> str:
    collection_name = "documents"
    collection = db[collection_name]
    result = collection.insert_one(document_data)

    # Return the ID of the inserted document
    return str(result.inserted_id)

"""
    This function performs the following operations:
    1. Calls `summarize_pdf` to get a summary of the document at the specified URL.
    2. Extracts the summary from the result and prepares the document data.
    3. Inserts the document data into the database and retrieves the document ID.
    4. Calls `create_chunks` to split the document into manageable chunks and stores them in the database.
"""
def process_one_document(user_id: str, folder_id: str, url: str):
    res = summarize_pdf(url)
    print(f"Received summary data: {res}")
    summary = res.get("summary", "")
    doc = Document(**res).model_dump()
    document_id = insert_document_to_db(doc)
    print(f"Document inserted with ID: {document_id}")
    create_chunks(user_id, folder_id, document_id, url, summary)
    print("Document processing complete.")
