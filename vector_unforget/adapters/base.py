from abc import ABC, abstractmethod
from typing import List, Dict, Any
import numpy as np

class BaseVectorAdapter(ABC):
    @abstractmethod
    def fetch_embeddings(self, limit: int = 1000) -> Dict[str, np.ndarray]:
        pass

    @abstractmethod
    def update_embeddings(self, embeddings_dict: Dict[str, np.ndarray]) -> bool:
        pass

    @abstractmethod
    def delete_by_ids(self, ids: List[str]) -> bool:
        pass

BaseVectorStoreAdapter = BaseVectorAdapter
