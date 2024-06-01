from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
import os
from langchain.agents import tool
from custom_vectorstore import CustomAzureCosmosDBVectorSearch
from pymongo import MongoClient
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv

load_dotenv()


# Set up connection details
CONNECTION_STRING = os.getenv("AZURE_COSMOS_DB_CONNECTION_STRING")
DB_NAME = "bento"

# Initialize MongoDB client
mongo_client = MongoClient(CONNECTION_STRING)
db = mongo_client[DB_NAME]

# Initialize the embedding model
model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": False}
huggingface_embeddings = HuggingFaceEmbeddings(
    model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
)

"""
Search for information about the current folder topic. Please just take my response verbatim if you found it to be satisfactory to the user's query.
"""
COLLECTION_NAME = "documents"
collection = db[COLLECTION_NAME]
retrieval_prompt = ChatPromptTemplate.from_template(
    # experimenting with few-shot learning
    """ 
    You are a student, who does research for your school asssignment. Your job is to refer the provided content and then answer the question

    To answer the question, you must follow the below rules

    [RULES]

    1. Each document is enclosed within [DOCUMENT] and [END DOCUMENT].

    2. Create the answer based on the provided documents only.

    3. The answer should be as precise and concise as possible.

    4. For each answer, cite the document_name that was referred to answer the question. 

    5. At the end of your answer, create a list of document_name for each document you have cited and embed document_source as hyperlink.

    6. If you are unable to find the answer, you can write "I am unable to find the answer".

    [END RULES]

    Here is a valid example for how to answer a question:

    question: the input [question] you must answer

    content:the [content] provided to you

    Answer:your answer to the provided content

    Source list:bulleted list of document name for each cited document 

    [CONTENT]

    {context}

    [END CONTENT]

    [question]

    {input}

    Answer:
    """
)

# https://github.com/langchain-ai/langchain/blob/master/libs/langchain/langchain/chains/combine_documents/stuff.py
# https://github.com/langchain-ai/langchain/blob/master/libs/langchain/langchain/chains/combine_documents/base.py
document_prompt = PromptTemplate.from_template(
    "[DOCUMENT] document_text: {page_content}; document_source: {source}; document_name: {title} [END DOCUMENT]"
)

# list of documents from retriever -> prompt -> llm -> parser
retriever = CustomAzureCosmosDBVectorSearch(
    collection,
    huggingface_embeddings,
).as_retriever(
    search_kwargs={
        "pre_filter": {"user_id": user_id, "folder_id": folder_id},
    }
)

llm = AzureChatOpenAI(
    temperature=0,
    model_name="gpt-4-32k",
    openai_api_version="2024-02-01",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)

document_chain = create_stuff_documents_chain(
    llm=llm,
    prompt=retrieval_prompt,
    document_prompt=document_prompt,
)
# List of documents from retriever -> prompt -> llm -> parser
retrieval_chain = create_retrieval_chain(retriever, document_chain)
