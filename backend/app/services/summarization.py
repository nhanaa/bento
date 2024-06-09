# Code is inspired by/copied from Greg Kamradt (Data Indy) and https://github.com/pashpashpash
from langchain_openai import AzureChatOpenAI
import os
from dotenv import load_dotenv
from typing import List
import json

load_dotenv()
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import numpy as np
from sklearn.cluster import KMeans
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
import json
from langchain_community.document_loaders import WebBaseLoader
from pymongo import MongoClient
import certifi


CONNECTION_STRING = os.getenv("AZURE_COSMOS_DB_CONNECTION_STRING")
DB_NAME = "bento"

# Initialize MongoDB client
mongo_client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())
db = mongo_client[DB_NAME]


# @app.post("/summarize/", response_model=SummarizeOutput)
def summarize_pdf(url: str) -> dict:
    print("************************************")
    print("Loading the language model...")
    print("************************************")
    llm = AzureChatOpenAI(
        temperature=0,
        model_name="gpt-4-32k",
        openai_api_version="2024-02-01",
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    )

    model_name = "sentence-transformers/all-mpnet-base-v2"
    model_kwargs = {"device": "cpu"}
    encode_kwargs = {"normalize_embeddings": False}
    huggingface_embeddings = HuggingFaceEmbeddings(
        model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
    )

    print("************************************")
    print("Loading PDF...")
    print("************************************")
    # url = "https://arxiv.org/pdf/1703.06870"
    loader = WebBaseLoader(url)
    # loader = WebBaseLoader(url, verify_ssl=False)
    pages = loader.load()
    print(f"Loaded {len(pages)} pages from the PDF.")

    text = ""
    for page in pages:
        text += page.page_content

    text = text.replace("\t", " ")

    print("************************************")
    print("Splitting text into chunks...")
    print("************************************")
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", "\t"], chunk_size=4000, chunk_overlap=500
    )

    docs: List[Document] = text_splitter.create_documents([text])
    print(f"Created {len(docs)} document chunks.")

    print("************************************")
    print("Embedding documents...")
    print("************************************")
    vectors: List[List[float]] = huggingface_embeddings.embed_documents(
        [x.page_content for x in docs]
    )

    num_clusters = 5
    print(f"Performing K-means clustering with {num_clusters} clusters...")
    kmeans = KMeans(n_clusters=num_clusters, random_state=42).fit(vectors)

    closest_indices = []
    print("Finding closest document to each cluster center...")
    for i in range(num_clusters):
        distances = np.linalg.norm(vectors - kmeans.cluster_centers_[i], axis=1)
        closest_index = np.argmin(distances)
        closest_indices.append(closest_index)

    selected_indices = sorted(closest_indices)
    print(f"Selected indices for summarization: {selected_indices}")

    map_prompt = """
    You will be given a single passage of a book/research paper/web content. In another word, long text will be chunked into smaller parts and you will be given a single chunk of text. 
    This section will be enclosed in triple backticks (```)
    Your goal is to give a summary of this section so that a reader will have a full understanding of what happened.
    Your response should be at least three paragraphs and fully encompass what was said in the passage.

    ```{text}```
    FULL SUMMARY:
    """
    map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text"])

    print("************************************")
    print("Generating summaries for selected document chunks...")
    print("************************************")
    # summary_list = []
    # for idx, val in enumerate(selected_indices):
    #     print(f"Processing cluster {idx} using {val}th chunk...")
    #     single_chain = map_prompt_template | llm | StrOutputParser()
    #     res = single_chain.invoke({"text": docs[val].page_content})
    #     summary_list.append(res)

    chain = (
        {"text": lambda idx: docs[idx].page_content}
        | map_prompt_template
        | llm
        | StrOutputParser()
    )
    summary_list = chain.batch(selected_indices, config={"max_concurrency": 5})

    summaries = "\n".join(summary_list)
    print("Summaries generated for all selected chunks.")
    # print(summaries)

    schema = {
        "type": "object",
        "properties": {
            "summary": {
                "type": "string",
                "description": "A summary of the content.",
            },
            "title": {
                "type": "string",
                "description": "The title of the content. File extension is PDF and the file names are limited to 64 characters",
            },
        },
        "required": ["summary", "title"],
    }
    schema_str = json.dumps(schema)

    question = """
    You will be provided with a single, unified summary that amalgamates various sections of a document. This document could be a book, research paper, or a web article. Your task is to analyze this summary and determine the type of medium it represents. Then, craft a comprehensive summary that aligns with the nature of the identified medium. Your final output should not include any explanation of how you determined the medium type.

    The summary is provided below enclosed in triple backticks for clarity:
    Summaries to analyze:
    ```{summaries}``` 

    Please respond only with the final output formatted as a JSON instance that conforms to the JSON schema provided below. Do not include any additional explanations or interpretations about how you identified the medium or generated the summary. The JSON output should be the only content in your response.

    Output should conform to the following JSON schema:
    ```{schema}```
    """.format(
        summaries=summaries, schema=schema_str
    )

    output = llm.invoke(question)
    print("************************************")
    print("Verbose summary generated.")
    print("************************************")
    content = output.content
    print(content)
    return json.loads(output.content)
