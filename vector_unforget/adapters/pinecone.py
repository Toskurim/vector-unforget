"""
Pinecone Vector Database Adapter for VectorUnforget.
Author: Toskurim
License: AGPLv3
"""

from typing import List, Dict, Any, Optional
from .base import BaseVectorAdapter


class PineconeAdapter(BaseVectorAdapter):
    """
    Adapter for Pinecone index interactions, supporting metadata-based
    cascading erasure, query probing, and vector hard deletes.
    """

    def __init__(self, index, namespace: str = ""):
        """
        :param index: A connected pinecone.Index instance.
        :param namespace: Pinecone namespace to operate on (default empty string).
        """
        self.index = index
        self.namespace = namespace

    def fetch_all_documents(self) -> List[Dict[str, Any]]:
        """
        Fetches/scans all available records with metadata from the index namespace.
        """
        formatted = []
        try:
            if hasattr(self.index, "scan_records"):
                records = self.index.scan_records(namespace=self.namespace)
            elif hasattr(self.index, "records"):
                records = self.index.records
            else:
                records = []

            for rec in records:
                if isinstance(rec, dict):
                    rec_id = rec.get("id")
                    meta = rec.get("metadata", {})
                    text = meta.get("text", "") or meta.get("content", "")
                else:
                    rec_id = getattr(rec, "id", None)
                    meta = getattr(rec, "metadata", {})
                    text = meta.get("text", "") or meta.get("content", "")

                formatted.append({
                    "id": str(rec_id),
                    "text": text,
                    "metadata": meta,
                })
        except Exception:
            pass

        return formatted

    def delete_documents_by_ids(self, ids: List[str]) -> bool:
        """
        Hard deletes vector records by ID from the Pinecone index namespace.
        """
        if not ids:
            return True

        try:
            if hasattr(self.index, "delete"):
                self.index.delete(ids=ids, namespace=self.namespace)
            return True
        except Exception:
            return False

    def query_text(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Queries the Pinecone index using mock or native search.
        """
        results = []
        try:
            if hasattr(self.index, "query_text"):
                raw = self.index.query_text(query, top_k=limit, namespace=self.namespace)
                for match in getattr(raw, "matches", []):
                    results.append({
                        "id": getattr(match, "id", str(match)),
                        "text": getattr(match, "metadata", {}).get("text", ""),
                        "metadata": getattr(match, "metadata", {}),
                    })
            elif hasattr(self.index, "query"):
                raw = self.index.query(vector=[0.0] * 8, top_k=limit, namespace=self.namespace, include_metadata=True)
                for match in getattr(raw, "matches", []):
                    results.append({
                        "id": match.id,
                        "text": match.metadata.get("text", "") if match.metadata else "",
                        "metadata": match.metadata or {},
                    })
        except Exception:
            pass
        return results

    def find_records_by_terms(self, terms: List[str], text_field: str = "text") -> List[Dict[str, Any]]:
        """
        Identifies vector records containing any target terms in their text content.
        """
        clean_terms = [t.lower() for t in terms if t.strip()]
        matched_records = []
        docs = self.fetch_all_documents()

        for doc in docs:
            content = doc.get("text", "").lower()
            for term in clean_terms:
                if term in content:
                    matched_records.append({
                        "id": doc.get("id"),
                        "matched_term": term,
                        "metadata": doc.get("metadata", {}),
                    })
                    break

        return matched_records

    def delete_records(self, ids: List[str], dry_run: bool = False) -> Dict[str, Any]:
        """
        Wrapper supporting dry-run simulation and real deletion.
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