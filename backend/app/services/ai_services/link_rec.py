from typing import List, Dict
from app import db
from utils.ai_tools import huggingface_embeddings
from .vectorstore_manager import VectorStoreWithFilter

# # Load environment variables from a .env file
# load_dotenv()


class LinkRec:
    collection_name = "browsing_history"
    embedding_key = "website_vector_field"

    def __init__(self):
        # Initialize the vector store
        filter_index_defs = [{"key": {"ip": 1}, "name": "ip_filter"}]
        self.vectorstore = VectorStoreWithFilter(
            self.collection_name,
            self.embedding_key,
            filter_index_defs=filter_index_defs,
            # look for the url to return as page content, the rest will be considered metadata
            text_key="url",
        )

    def get_links(self, ip: str, desc: str) -> Dict[str, List[str]]:
        similar_documents = self.vectorstore.search_similarity(
            query=desc, filter_dict={"ip": ip}
        )
        # Return the search results
        return {"links_list": [doc.page_content for doc in similar_documents]}

    def embed_browsing_history(self, data):
        """
        Takes in a dict of browsing history and embed its url + title
        """
        for item in data:
            url_in_str = str(item["url"])
            my_str = item["title"] + " " + url_in_str
            item["url"] = url_in_str
            item[self.embedding_key] = huggingface_embeddings.embed_query(my_str)
        return data
