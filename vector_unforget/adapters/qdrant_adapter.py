from typing import List, Dict, Any
import numpy as np
from vector_unforget.adapters.base import BaseVectorAdapter

class QdrantAdapter(BaseVectorAdapter):
    def __init__(self, client: Any, collection_name: str):
        self.client = client
        self.collection_name = collection_name

    def fetch_embeddings(self, limit: int = 1000) -> Dict[str, np.ndarray]:
        if hasattr(self.client, "scroll"):
            records, _ = self.client.scroll(collection_name=self.collection_name, limit=limit, with_vectors=True)
            res = {}
            for point in records:
                vec = point.vector if hasattr(point, "vector") else point.get("vector")
                pid = str(point.id if hasattr(point, "id") else point.get("id"))
                if vec is not None:
                    res[pid] = np.array(vec, dtype=np.float32)
            return res
        return {}

    def update_embeddings(self, embeddings_dict: Dict[str, np.ndarray]) -> bool:
        if not embeddings_dict:
            return True
        if hasattr(self.client, "update_vectors"):
            try:
                from qdrant_client.http import models as rest_models
                points = [rest_models.PointVectors(id=pid, vector=vec.tolist()) for pid, vec in embeddings_dict.items()]
                self.client.update_vectors(collection_name=self.collection_name, points=points)
            except Exception:
                pass
            return True
        return True

    def delete_by_ids(self, ids: List[str]) -> bool:
        if hasattr(self.client, "delete"):
            try:
                from qdrant_client.http import models as rest_models
                self.client.delete(collection_name=self.collection_name, points_selector=rest_models.PointIdsList(points=ids))
            except Exception:
                pass
            return True
        return True
