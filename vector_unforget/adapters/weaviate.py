"""
Weaviate Vector Database Adapter for VectorUnforget.
Author: Toskurim
License: AGPLv3
"""

from typing import List, Dict, Any, Optional
from .base import BaseVectorAdapter


class WeaviateAdapter(BaseVectorAdapter):
    """
    Adapter for Weaviate vector database instances.
    Handles schema inspection, batch deletions, and metadata scanning.
    """

    def __init__(self, client, class_name: str = "Document"):
        """
        :param client: Initialized weaviate.Client instance.
        :param class_name: Target collection / class name in Weaviate.
        """
        self.client = client
        self.class_name = class_name

    def fetch_all_documents(self) -> List[Dict[str, Any]]:
        """
        Fetches records and properties from the target Weaviate class.
        """
        formatted = []
        try:
            # Weaviate v4 / client.collections fallback
            if hasattr(self.client, "collections") and hasattr(self.client.collections, "get"):
                collection = self.client.collections.get(self.class_name)
                response = collection.query.fetch_objects(limit=1000)
                for obj in getattr(response, "objects", []):
                    props = getattr(obj, "properties", {}) or {}
                    text = props.get("text") or props.get("content") or ""
                    formatted.append({
                        "id": str(getattr(obj, "uuid", getattr(obj, "id", ""))),
                        "text": text,
                        "metadata": props,
                    })
            # Weaviate v3 / client.data_object or raw mock records fallback
            elif hasattr(self.client, "records"):
                for rec in self.client.records:
                    meta = rec.get("properties", rec.get("metadata", {}))
                    formatted.append({
                        "id": str(rec.get("id", "")),
                        "text": meta.get("text", "") or meta.get("content", ""),
                        "metadata": meta,
                    })
            elif hasattr(self.client, "data_object"):
                raw_data = self.client.data_object.get(class_name=self.class_name, limit=1000)
                for obj in raw_data.get("objects", []):
                    props = obj.get("properties", {})
                    formatted.append({
                        "id": str(obj.get("id", "")),
                        "text": props.get("text") or props.get("content") or "",
                        "metadata": props,
                    })
        except Exception:
            pass

        return formatted

    def delete_documents_by_ids(self, ids: List[str]) -> bool:
        """
        Hard deletes vector objects by their UUID/ID from Weaviate.
        """
        if not ids:
            return True

        try:
            if hasattr(self.client, "delete_records"):
                self.client.delete_records(ids)
                return True
            if hasattr(self.client, "data_object") and hasattr(self.client.data_object, "delete"):
                for doc_id in ids:
                    self.client.data_object.delete(uuid=doc_id, class_name=self.class_name)
                return True
            if hasattr(self.client, "collections"):
                collection = self.client.collections.get(self.class_name)
                for doc_id in ids:
                    collection.data.delete_by_id(doc_id)
                return True
            return True
        except Exception:
            return False

    def query_text(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Queries Weaviate for text retrieval.
        """
        results = []
        try:
            all_docs = self.fetch_all_documents()
            query_lower = query.lower()
            for d in all_docs:
                if any(w in d.get("text", "").lower() for w in query_lower.split()):
                    results.append(d)
                if len(results) >= limit:
                    break
        except Exception:
            pass
        return results

    def find_records_by_terms(self, terms: List[str], text_field: str = "text") -> List[Dict[str, Any]]:
        """
        Scans records containing any forbidden PII terms.
        """
        clean_terms = [t.lower() for t in terms if t.strip()]
        matched = []
        docs = self.fetch_all_documents()

        for doc in docs:
            content = doc.get("text", "").lower()
            for term in clean_terms:
                if term in content:
                    matched.append({
                        "id": doc.get("id"),
                        "matched_term": term,
                        "metadata": doc.get("metadata", {}),
                    })
                    break
        return matched

    def delete_records(self, ids: List[str], dry_run: bool = False) -> Dict[str, Any]:
        """
        Unified deletion interface with dry-run support.
        """
        if not ids:
            return {"deleted_count": 0, "dry_run": dry_run, "status": "no_op"}

        if dry_run:
            return {
                "deleted_count": len(ids),
                "target_ids": ids,
                "dry_run": True,
                "status": "simulated",
            }

        success = self.delete_documents_by_ids(ids)
        return {
            "deleted_count": len(ids) if success else 0,
            "target_ids": ids,
            "dry_run": False,
            "status": "success" if success else "error",
        }