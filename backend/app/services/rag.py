from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
import os
from langchain.agents import tool
from pymongo import MongoClient
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv

# import from local module
from .prompt import retrieval_prompt, document_prompt
from ..utils.ai_tools import llm
from .vectorstore_manager import VectorStoreManager
from ..app import db

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
        CHUNK_COLLECTION_NAME = "chunks"
        embedding_key = "vectorContent"
        chunk_collection = db[CHUNK_COLLECTION_NAME]
        vector_manager = VectorStoreManager(chunk_collection, embedding_key)
        retriever = vector_manager.get_retriever(user_id, folder_id)

        logger.info("Initialized document retriever")

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
