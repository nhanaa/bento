import os
import logging
from dotenv import load_dotenv
from pymongo import MongoClient
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.agents import tool, AgentExecutor, create_openai_functions_agent
from custom_vectorstore import CustomAzureCosmosDBVectorSearch
from langchain_community.embeddings import HuggingFaceEmbeddings
from rag import custom_create_retrieval_chain
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.runnables.history import (
    RunnableWithMessageHistory,
    ConfigurableFieldSpec,
)
from prompt import agent_prompt
from langchain_community.chat_message_histories.cosmos_db import (
    CosmosDBChatMessageHistory,
)
from langchain_openai import AzureChatOpenAI

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB client setup
CONNECTION_STRING = os.getenv("AZURE_COSMOS_DB_CONNECTION_STRING")
mongo_client = MongoClient(CONNECTION_STRING)
db = mongo_client["bento"]
logger.info("Connected to MongoDB")

# HuggingFace Embeddings initialization
model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": False}
huggingface_embeddings = HuggingFaceEmbeddings(
    model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
)
logger.info("Initialized HuggingFace embeddings")


def create_agent(user_id, folder_id):
    retrieval_chain = custom_create_retrieval_chain(user_id, folder_id)

    # Define tools
    @tool
    def retriever_doc(query: str) -> str:
        """
        Search for information about the current folder topic. Please just take my response verbatim if you found it to be satisfactory to the user's query.
        """
        try:
            response = retrieval_chain.invoke({"input": query})
            for doc in response["context"]:
                logger.info(f"Retrieved document: {doc['metedata']['']}")
            return response["answer"]
        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            raise e

    search = TavilySearchResults()
    tools = [retriever_doc, search]

    # Initialize Azure OpenAI
    llm = AzureChatOpenAI(
        temperature=0,
        model_name="gpt-4-32k",
        openai_api_version="2024-02-01",
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    )
    logger.info("Initialized AzureChatOpenAI")

    # Create agent and executor
    agent = create_openai_functions_agent(llm, tools, prompt=agent_prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        return_intermediate_steps=True,
        handle_parsing_errors=True,
    )

    # CosmosDB setup for chat history
    cosmos_database = "chatbot_db"
    cosmos_container = "chatbot_container"

    def get_message_history(user_id: str, folder_id: str) -> CosmosDBChatMessageHistory:
        try:
            chat_history = CosmosDBChatMessageHistory(
                cosmos_database=cosmos_database,
                cosmos_container=cosmos_container,
                session_id=folder_id,
                user_id=user_id,
                cosmos_endpoint=os.getenv("CHAT_AZURE_COSMOS_DB_ENDPOINT"),
                connection_string=os.getenv("CHAT_AZURE_COSMOS_DB_CONNECTION_STRING"),
            )
            chat_history.prepare_cosmos()
            logger.info(
                f"Prepared CosmosDB chat history for user: {user_id}, session: {folder_id}"
            )
            return chat_history
        except Exception as e:
            logger.error(f"Error setting up chat history: {str(e)}")
            raise e

    # Create agent with chat history
    agent_with_chat_history = RunnableWithMessageHistory(
        agent_executor,
        get_session_history=get_message_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        history_factory_config=[
            ConfigurableFieldSpec(
                id="user_id",
                annotation=str,
                name="User ID",
                description="Unique identifier for the user.",
                default="",
                is_shared=True,
            ),
            ConfigurableFieldSpec(
                id="folder_id",
                annotation=str,
                name="Conversation ID",
                description="Unique identifier for the conversation.",
                default="",
                is_shared=True,
            ),
        ],
    )
    logger.info("Agent with chat history is set up and ready to use")
    return agent_with_chat_history
