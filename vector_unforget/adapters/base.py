"""
Base Vector Store Adapter Interface for VectorUnforget.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import numpy as np


class BaseVectorAdapter(ABC):
    """
    Abstract base class defining the contract for vector database integrations.
    Provides backward compatibility for all methods across the adapter suite.
    """

    def fetch_embeddings(self, limit: int = 1000) -> Dict[str, np.ndarray]:
        """Fetch vectors with IDs from the storage."""
        return {}

    def update_embeddings(self, embeddings_dict: Dict[str, np.ndarray]) -> bool:
        """Update vectors in-place after orthogonal unlearning."""
        return True

    def delete_by_ids(self, ids: List[str]) -> bool:
        """Delete records explicitly by ID list."""
        if hasattr(self, "delete_records"):
            return self.delete_records(ids)
        return True

    def delete_records(self, ids: List[str]) -> bool:
        """Legacy deletion method."""
        return True

    def delete(self, *args, **kwargs) -> Any:
        """Generic delete proxy."""
        return True

    def fetch_documents(self, *args, **kwargs) -> Any:
        """Document retrieval proxy."""
        return []
