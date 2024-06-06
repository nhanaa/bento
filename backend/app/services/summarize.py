# Code is inspired by/copied from Greg Kamradt (Data Indy) and https://github.com/pashpashpash
from langchain_openai import AzureChatOpenAI
import os
from dotenv import load_dotenv
from typing import List

load_dotenv()
from langchain.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import numpy as np
from sklearn.cluster import KMeans
from langchain import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
from langchain_core.documents import Document
import json

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
url = "https://arxiv.org/pdf/2404.16821v2"
loader = PyPDFLoader(url)
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

summary_list = []
print("************************************")
print("Generating summaries for selected document chunks...")
print("************************************")
for idx, val in enumerate(selected_indices):
    print(f"Processing cluster {idx} using {val}th chunk...")
    single_chain = map_prompt_template | llm | StrOutputParser()
    res = single_chain.invoke({"text": docs[val].page_content})
    summary_list.append(res)

summaries = "\n".join(summary_list)
print("Summaries generated for all selected chunks.")

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

question = """You will be given a series of summaries extracted from a book, research paper, or web content, etc. Your task is to identify the type of medium these summaries belong to (book, research paper, web content, etc). Once identified, provide a comprehensive summary that aligns with the nature of the identified medium. Do not tell the user how you came up with that conclusion. The summaries will be enclosed in triple backticks (```). Your goal is to deliver a detailed and verbose summary that thoroughly conveys the content. The reader should gain a clear and complete understanding of what the original material covered.
There is no length limit. Here are the summaries: ```{summaries}``` \n
Output instructions: 
The output should be formatted as a JSON instance that conforms to the JSON schema below.

As an example, for the schema {{"properties": {{"foo": {{"title": "Foo", "description": "a list of strings", "type": "array", "items": {{"type": "string"}}}}}}, "required": ["foo"]}}
the object {{"foo": ["bar", "baz"]}} is a well-formatted instance of the schema. The object {{"properties": {{"foo": ["bar", "baz"]}}}} is not well-formatted.

Here is the output schema:
```
{schema}
```
""".format(
    summaries=summaries, schema=schema_str
)

chain = llm | StrOutputParser()
output = chain.invoke(question)
print("************************************")
print("Verbose summary generated.")
print("************************************")
print(output)
