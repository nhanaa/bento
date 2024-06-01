from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
import os
from langchain.agents import tool, AgentExecutor, create_openai_functions_agent
from custom_vectorstore import CustomAzureCosmosDBVectorSearch
from pymongo import MongoClient
from langchain_community.embeddings import HuggingFaceEmbeddings
from rag import retrieval_chain
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.runnables.history import (
    RunnableWithMessageHistory,
    ConfigurableFieldSpec,
)
from langchain_community.chat_message_histories.cosmos_db import (
    CosmosDBChatMessageHistory,
)
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


@tool
def retriever_doc(query: str) -> str:
    response = retrieval_chain.invoke({"input": query})
    # response has 3 fields: input (propmt); context: list of documents; answer: the llm repsonse
    print(f"I obtained the following documents {response['context']}")
    return response["answer"]


search = TavilySearchResults()
tools = [retriever_doc, search]

agent_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a highly helpful learning assistant within a learning platform. This platform is organized into numerous folders, each containing a specific topic, such as econometrics or deontological ethics.
            Within each folder's dashboard, learners can access general knowledge or information relevant to the current folder.
            This includes links from browsing history, downloaded files, or screenshots. Answer the following questions to the best of your ability. Feel free to utilize any of the provided tools. 
            However, always use the retriever_doc tool if the question is about the current folder and the folder topic: {folder_topic}. 
            """,
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

llm = AzureChatOpenAI(
    temperature=0,
    model_name="gpt-4-32k",
    openai_api_version="2024-02-01",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)

# prompt.pretty_print() -> basically contains 1) history 2) system prompt: you are a helpful assistant 3) input 4) agent_scratchpad
agent = create_openai_functions_agent(llm, tools, prompt=agent_prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    return_intermediate_steps=True,
    handle_parsing_errors=True,
)

cosmos_database = "chatbot_db"
cosmos_container = "chatbot_container"


def get_message_history(user_id: str, session_id: str) -> CosmosDBChatMessageHistory:
    chat_history = CosmosDBChatMessageHistory(
        cosmos_database=cosmos_database,
        cosmos_container=cosmos_container,
        session_id=session_id,
        user_id=user_id,
        cosmos_endpoint=os.getenv("CHAT_AZURE_COSMOS_DB_ENDPOINT"),
        connection_string=os.getenv("CHAT_AZURE_COSMOS_DB_CONNECTION_STRING"),
    )
    chat_history.prepare_cosmos()
    return chat_history


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
