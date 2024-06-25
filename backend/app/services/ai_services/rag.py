from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from dotenv import load_dotenv
import logging
from typing import Optional

# import from local module
from .prompt import retrieval_prompt, document_prompt
from utils.ai_tools import llm
from .vectorstore_manager import VectorStoreWithFilter
from app import db

load_dotenv()


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
        collection_name = "chunks"
        embedding_key = "vectorContent"
        filter_index_defs = [
            {"key": {"user_id": 1}, "name": "user_filter"},
            {"key": {"folder_id": 1}, "name": "folder_filter"},
        ]
        vector_manager = VectorStoreWithFilter(
            collection_name, embedding_key, filter_index_defs=filter_index_defs
        )
        retriever = vector_manager.get_retriever(
            filter_dict={"user_id": user_id, "folder_id": folder_id}
        )

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
