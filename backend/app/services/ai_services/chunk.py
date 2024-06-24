from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from .vectorstore_manager import VectorStoreWithFilter

"""
For ONE given website url, document id, and document summary, create and add chunks to vector db
user id, folder_id
"""


class Chunk:
    collection_name = "chunks"
    embedding_key = "vectorContent"

    def __init__(self):
        filter_index_defs = [
            {"key": {"user_id": 1}, "name": "user_filter"},
            {"key": {"folder_id": 1}, "name": "folder_filter"},
        ]
        vector_manager = VectorStoreWithFilter(
            self.collection_name,
            self.embedding_key,
            filter_index_defs=filter_index_defs,
        )
        self.chunk_vectorstore = vector_manager.get_vectorstore()

    async def create_chunks(
        self, user_id: str, folder_id: str, document_id: str, url: str, doc_summary: str
    ):
        print(f"my doc summary is {doc_summary}")
        loader = WebBaseLoader(
            web_path=url,
            verify_ssl=False,
            bs_get_text_kwargs={"strip": True, "separator": " "},
        )
        document_list = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
        docs = text_splitter.split_documents(document_list)

        # Add metadata to the documents
        for doc in docs:
            doc.page_content += doc_summary
            doc.metadata.update(
                {"user_id": user_id, "folder_id": folder_id, "document_id": document_id}
            )
        print(f"one example doc is {docs[0]}")

        # Add the documents to the vector store
        await self.chunk_vectorstore.aadd_documents(docs)
