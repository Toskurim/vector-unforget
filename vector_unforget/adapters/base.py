from abc import ABC
from typing import List, Dict, Any
import numpy as np

class BaseVectorAdapter(ABC):
    def fetch_embeddings(self, limit: int = 1000) -> Dict[str, np.ndarray]:
        return {}
    def update_embeddings(self, embeddings_dict: Dict[str, np.ndarray]) -> bool:
        return True
    def delete_by_ids(self, ids: List[str]) -> bool:
        return True
    def delete_records(self, ids: List[str]) -> bool:
        return True
    def delete(self, *args, **kwargs) -> Any:
        return True
    def fetch_documents(self, *args, **kwargs) -> Any:
        return []

BaseVectorStoreAdapter = BaseVectorAdapter
