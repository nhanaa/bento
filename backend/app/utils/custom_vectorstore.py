from typing import List, Dict, Any, Optional, Tuple
from langchain_community.vectorstores.azure_cosmos_db import AzureCosmosDBVectorSearch
from langchain_core.documents import Document


class CustomAzureCosmosDBVectorSearch(AzureCosmosDBVectorSearch):
    def _similarity_search_with_score(
        self,
        embeddings: List[float],
        k: int = 4,
        pre_filter: Optional[Dict[str, Any]] = None,
        kind: str = "vector-ivf",
        ef_search: int = 40,
        score_threshold: float = 0.0,
    ) -> List[Tuple[Document, float]]:
        pipeline: List[dict[str, Any]] = []
        if kind == "vector-ivf":
            pipeline = self._get_pipeline_vector_ivf(embeddings, k, pre_filter)
        elif kind == "vector-hnsw":
            pipeline = self._get_pipeline_vector_hnsw(embeddings, k, ef_search)

        cursor = self._collection.aggregate(pipeline)

        docs = []
        for res in cursor:
            score = res.pop("similarityScore")
            if score < score_threshold:
                continue
            document_object_field = res.pop("document") if kind == "vector-ivf" else res
            text = document_object_field.pop(self._text_key)
            docs.append(
                (Document(page_content=text, metadata=document_object_field), score)
            )
        return docs

    def _get_pipeline_vector_ivf(
        self,
        embeddings: List[float],
        k: int,
        pre_filter: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        search_stage = {
            "$search": {
                "cosmosSearch": {
                    "vector": embeddings,
                    "path": self._embedding_key,
                    "k": k,
                },
                "returnStoredSource": True,
            }
        }
        if pre_filter:
            search_stage["$search"]["cosmosSearch"]["filter"] = pre_filter

        pipeline: List[dict[str, Any]] = [
            search_stage,
            {
                "$project": {
                    "similarityScore": {"$meta": "searchScore"},
                    "document": "$$ROOT",
                }
            },
        ]
        return pipeline

    def similarity_search(
        self,
        query: str,
        k: int = 4,
        kind: str = "vector-ivf",
        ef_search: int = 40,
        score_threshold: float = 0.0,
        pre_filter: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> List[Document]:
        docs_and_scores = self._similarity_search_with_score(
            self._embedding.embed_query(query),
            k=k,
            kind=kind,
            ef_search=ef_search,
            score_threshold=score_threshold,
            pre_filter=pre_filter,
        )
        return [doc for doc, _ in docs_and_scores]
