from prompt import retrieval_prompt, document_prompt
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
import os
from langchain.agents import tool
from custom_vectorstore import CustomAzureCosmosDBVectorSearch
from pymongo import MongoClient
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
import certifi

load_dotenv()

import logging
from typing import Optional


def custom_create_retrieval_chain(
    user_id: str, folder_id: str
) -> Optional[create_retrieval_chain]:
    """
    Create a retrieval chain for document processing and querying.

    Args:
        user_id (str): The ID of the user.
        folder_id (str): The ID of the folder.

    Returns:
        create_retrieval_chain: The initialized retrieval chain.
    """
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        # Set up connection details
        CONNECTION_STRING = os.getenv("AZURE_COSMOS_DB_CONNECTION_STRING")
        if not CONNECTION_STRING:
            logger.error(
                "AZURE_COSMOS_DB_CONNECTION_STRING environment variable is not set"
            )
            return None

        DB_NAME = "bento"

        # MongoDB client initialization
        mongo_client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())
        db = mongo_client[DB_NAME]
        logger.info("Connected to MongoDB")

        # Embedding model initialization
        model_name = "sentence-transformers/all-mpnet-base-v2"
        model_kwargs = {"device": "cpu"}
        encode_kwargs = {"normalize_embeddings": False}
        huggingface_embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs,
        )
        logger.info("Initialized HuggingFace embeddings")

        # Collection access
        COLLECTION_NAME = "documents"
        collection = db[COLLECTION_NAME]
        logger.info(f"Accessing collection: {COLLECTION_NAME}")

        # Document retrieval and processing
        retriever = CustomAzureCosmosDBVectorSearch(
            collection,
            huggingface_embeddings,
        ).as_retriever(
            search_kwargs={"pre_filter": {"user_id": user_id, "folder_id": folder_id}}
        )
        logger.info("Initialized document retriever")

        # Initialize Azure OpenAI
        llm = AzureChatOpenAI(
            temperature=0,
            model_name="gpt-4-32k",
            openai_api_version="2024-02-01",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        )
        if not llm:
            logger.error("AzureChatOpenAI initialization failed")
            return None
        logger.info("Initialized AzureChatOpenAI")

        # Create document and retrieval chains
        document_chain = create_stuff_documents_chain(
            llm=llm,
            prompt=retrieval_prompt,
            document_prompt=document_prompt,
        )
        retrieval_chain = create_retrieval_chain(retriever, document_chain)
        logger.info("Created document and retrieval chains")

        return retrieval_chain

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return None
