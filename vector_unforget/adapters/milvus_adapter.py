"""
Milvus Vector Database Adapter for VectorUnforget.
Supports batch deletion by scalar primary keys, expression filtering, and document querying.
"""

from typing import List, Dict, Any, Optional
from vector_unforget.adapters.base import BaseVectorAdapter

try:
    from pymilvus import Collection
    MILVUS_AVAILABLE = True
except ImportError:
    MILVUS_AVAILABLE = False


class MilvusAdapter(BaseVectorAdapter):
    """
    Adapter for purging embeddings and associated metadata from Milvus collections.
    """

    def __init__(
        self,
        collection: Any,
        pk_field: str = "id",
        text_field: str = "text",
        vector_field: str = "vector"
    ):
        """
        Initialize MilvusAdapter.

        Args:
            collection: An instance of pymilvus.Collection or a compatible mock object.
            pk_field: Name of the primary key field in the collection schema.
            text_field: Name of the raw document text field.
            vector_field: Name of the embedding vector field.
        """
        self.collection = collection
        self.pk_field = pk_field
        self.text_field = text_field
        self.vector_field = vector_field

    def fetch_all_documents(self, limit: int = 1000) -> List[Dict[str, Any]]:
        """
        Fetch documents from the Milvus collection for PII graph inspection.
        """
        expr = f"{self.pk_field} != ''"
        try:
            results = self.collection.query(
                expr=expr,
                output_fields=[self.pk_field, self.text_field, self.vector_field],
                limit=limit
            )
            documents = []
            for item in results:
                documents.append({
                    "id": item.get(self.pk_field),
                    "text": item.get(self.text_field, ""),
                    "vector": item.get(self.vector_field, None),
                    "metadata": {k: v for k, v in item.items() if k not in [self.pk_field, self.text_field, self.vector_field]}
                })
            return documents
        except Exception:
            return []

    def delete_documents_by_ids(
        self, doc_ids: List[str], dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Delete vectors associated with specified primary keys from the Milvus collection.
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

        formatted_ids = [f'"{i}"' if isinstance(i, str) else str(i) for i in doc_ids]
        expr = f"{self.pk_field} in [{', '.join(formatted_ids)}]"

        res = self.collection.delete(expr)
        deleted_count = getattr(res, "delete_count", len(doc_ids))

        return {
            "status": "success",
            "deleted_count": deleted_count,
            "expr": expr,
            "dry_run": False,
        }

    def delete_by_metadata_field(
        self, field: str, value: Any, dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Delete entities matching a scalar metadata attribute.
        """
        val_repr = f'"{value}"' if isinstance(value, str) else str(value)
        expr = f"{field} == {val_repr}"

        if dry_run:
            return {
                "status": "dry_run_success",
                "filter": expr,
                "dry_run": True,
            }

        res = self.collection.delete(expr)
        deleted_count = getattr(res, "delete_count", 0)

        return {
            "status": "success",
            "deleted_count": deleted_count,
            "expr": expr,
            "dry_run": False,
        }