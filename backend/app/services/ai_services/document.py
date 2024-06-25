from .summarization import summarize_website
from .chunk import Chunk
from models.rag_model import DocumentModel
from app import db
from asyncio import gather


class Document:
    def __init__(self):
        self.chunk = Chunk()

    async def insert_document_to_db(self, document_data: dict) -> str:
        collection_name = "documents"
        if collection_name not in db.list_collection_names():
            db.create_collection(collection_name)
        collection = db[collection_name]
        result = collection.insert_one(document_data)
        return str(result.inserted_id)

    async def process_one_document(self, user_id: str, folder_id: str, url: str):
        """
        This function performs the following operations:
        1. Calls `summarize_website` to get a summary of the document at the specified URL.
        2. Extracts the summary from the result and prepares the document data.
        3. Inserts the document data into the database and retrieves the document ID.
        4. Calls `create_chunks` to split the document into manageable chunks and stores them in the database.
        """
        res = await summarize_website(url)
        print(f"Received summary data: {res}")
        summary = res.get("summary", "")

        res["folder_id"] = folder_id
        res["user_id"] = user_id
        # checking that documnet follows the wanted format
        doc = DocumentModel(**res).model_dump()
        document_id = await self.insert_document_to_db(doc)
        print(f"Document inserted with ID: {document_id}")
        await self.chunk.create_chunks(user_id, folder_id, document_id, url, summary)
        print("Document processing complete.")

    async def process_many_documents(self, user_id, folder_id, data):
        tasks = [
            self.process_one_document(
                user_id=user_id, folder_id=folder_id, url=str(link)
            )
            for link in data
        ]

        await gather(*tasks)
