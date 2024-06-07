from whoosh.index import create_in
from whoosh.query import FuzzyTerm
from whoosh.fields import Schema, TEXT
from whoosh.qparser import QueryParser
from whoosh.filedb.filestore import RamStorage

class SearchEngine:
    def __init__(self):
        self.indexes = {}
        self.indexes['file'] = RamStorage().create_index(Schema(path=TEXT(stored=True), content=TEXT(stored=True)))
        self.indexes['folder'] = RamStorage().create_index(Schema(path=TEXT(stored=True), content=TEXT(stored=True)))

    def seed(self, type, documents):
        writer = self.indexes[type].writer()

        for path, content in documents:
            writer.add_document(path = path, content = content)
        writer.commit()

    def query(self, type, text):
        index = self.indexes[type]

        query_parser = QueryParser("content", index.schema, termclass=FuzzyTerm)
        query = query_parser.parse(text)
        results = index.searcher().search(query)
        
        # Extract and return the relevant information from search results
        search_results = []
        for hit in results:
            search_results.append({
                "score": hit.score,
                "path": hit["path"],
                "content": hit["content"]
            })
        
        return search_results