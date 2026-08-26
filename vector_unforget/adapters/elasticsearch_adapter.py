"""
Elasticsearch & OpenSearch Adapter for VectorUnforget.
Supports document fetching, ID/query-based deletion, and dense vector field scrubbing.
"""

from typing import List, Dict, Any, Optional
from vector_unforget.adapters.base import BaseVectorAdapter


class ElasticsearchAdapter(BaseVectorAdapter):
    """
    Adapter for purging embeddings and documents from Elasticsearch/OpenSearch indices.
    """

    def __init__(
        self,
        client: Any,
        index: str,
        text_field: str = "text",
        vector_field: str = "vector"
    ):
        """
        Initialize ElasticsearchAdapter.

        Args:
            client: An instance of elasticsearch.Elasticsearch, opensearchpy.OpenSearch, or a compatible mock.
            index: Target index name.
            text_field: Document field containing raw text.
            vector_field: Document field containing embedding vectors.
        """
        self.client = client
        self.index = index
        self.text_field = text_field
        self.vector_field = vector_field

    def fetch_all_documents(self, limit: int = 1000) -> List[Dict[str, Any]]:
        """
        Fetch documents from the Elasticsearch index.
        """
        query = {"match_all": {}}
        try:
            res = self.client.search(
                index=self.index,
                query=query,
                size=limit
            )
            hits = res.get("hits", {}).get("hits", [])
            documents = []
            for hit in hits:
                source = hit.get("_source", {})
                documents.append({
                    "id": hit.get("_id"),
                    "text": source.get(self.text_field, ""),
                    "vector": source.get(self.vector_field, None),
                    "metadata": {k: v for k, v in source.items() if k not in [self.text_field, self.vector_field]}
                })
            return documents
        except Exception:
            return []

    def delete_documents_by_ids(
        self, doc_ids: List[str], dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Delete documents by _id using delete_by_query.
        """
        if not doc_ids:
            return {"status": "noop", "deleted_count": 0, "dry_run": dry_run}

        if dry_run:
            return {
                "status": "dry_run_success",
                "deleted_count": len(doc_ids),
                "target_ids": doc_ids,
                "dry_run": True,
            }

        query = {"ids": {"values": doc_ids}}
        res = self.client.delete_by_query(index=self.index, query=query)
        deleted_count = res.get("deleted", len(doc_ids))

        return {
            "status": "success",
            "deleted_count": deleted_count,
            "dry_run": False,
        }

    def delete_by_metadata_field(
        self, field: str, value: Any, dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Delete documents matching a specific metadata field term.
        """
        query = {"term": {field: value}}

        if dry_run:
            return {
                "status": "dry_run_success",
                "filter": query,
                "dry_run": True,
            }

        res = self.client.delete_by_query(index=self.index, query=query)
        deleted_count = res.get("deleted", 0)

        return {
            "status": "success",
            "deleted_count": deleted_count,
            "dry_run": False,
        }