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


from app import db
from utils.ai_tools import huggingface_embeddings


# # Load environment variables from a .env file
# load_dotenv()


class LinkRec:
    def __init__(self):
        COLLECTION_NAME = "browsing_history_test"
        self.collection = db[COLLECTION_NAME]

        # Initialize the vector store
        self.vectorstore = AzureCosmosDBVectorSearch(
            collection=self.collection,
            embedding=huggingface_embeddings,
            index_name="website_vector_index",
            embedding_key="website_vector_field",
            # look for the url to return as page content, the rest will be considered metadata
            text_key="url",
        )
        if not self.vectorstore.index_exists():
            self.vectorstore.create_index(dimensions=768)

    def get_links(self, user_id: str, desc: str) -> Dict[str, List[str]]:
        similar_documents = self.vectorstore.similarity_search(
            desc, score_threshold=0.35, k=6
        )
        # Return the search results
        return {"links_list": [doc.page_content for doc in similar_documents]}

    def insert_browsing_history(self, data):
        """
        Inserts the browsing history data into the Azure Cosmos DB.
        """
        # Insert the data into the collection
        for item in data:
            # my_dict = item.model_dump()
            my_dict = item
            url_in_str = str(my_dict["url"])
            my_str = my_dict["title"] + " " + url_in_str
            my_dict["url"] = url_in_str
            my_dict["website_vector_field"] = huggingface_embeddings.embed_query(my_str)
            self.collection.insert_one(my_dict)
