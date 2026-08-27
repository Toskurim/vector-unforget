"""
ChromaDB Vector Database Adapter for VectorUnforget.
"""

from typing import List, Dict, Any, Optional
import numpy as np
from vector_unforget.adapters.base import BaseVectorStoreAdapter


class ChromaAdapter(BaseVectorStoreAdapter):
    """
    Adapter for ChromaDB open-source embedding database.
    """

    def __init__(self, collection: Any):
        self.collection = collection

    def fetch_embeddings(self, limit: int = 1000) -> Dict[str, np.ndarray]:
        """
        Fetch vectors with IDs from the Chroma collection.
        """
        if hasattr(self.collection, "get"):
            data = self.collection.get(include=["embeddings"], limit=limit)
            ids = data.get("ids", [])
            embeddings = data.get("embeddings", [])
            res = {}
            if embeddings is not None:
                for pid, emb in zip(ids, embeddings):
                    if emb is not None:
                        res[str(pid)] = np.array(emb, dtype=np.float32)
            return res
        return {}

    def update_embeddings(self, embeddings_dict: Dict[str, np.ndarray]) -> bool:
        """
        Update vectors in-place in Chroma collection.
        """
        if not embeddings_dict:
            return True
        if hasattr(self.collection, "update"):
            ids = list(embeddings_dict.keys())
            embeddings = [vec.tolist() for vec in embeddings_dict.values()]
            self.collection.update(ids=ids, embeddings=embeddings)
            return True
        return True

    def delete_by_ids(self, ids: List[str]) -> bool:
        """
        Delete records explicitly by ID list.
        """
        if hasattr(self.collection, "delete"):
            self.collection.delete(ids=ids)
            return True
        return True
