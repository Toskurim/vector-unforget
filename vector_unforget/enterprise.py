"""
Enterprise enhancements for VectorUnforget:
- Metadata-scoped entity disambiguation (Homonym resolution)
- Reversible Delta Ledger & Safe Rollback Buffer
"""
import time
import hashlib
from typing import Dict, List, Optional, Any, Tuple
import numpy as np

class MetadataScopedScrubber:
    """
    Resolves homonym collisions by enforcing strict metadata predicate isolation
    before computing concept centroids and subspace projections.
    """
    def __init__(self, embedding_dim: int = 1536):
        self.embedding_dim = embedding_dim

    def filter_and_extract_centroid(
        self,
        embeddings: np.ndarray,
        metadata_list: List[Dict[str, Any]],
        target_entity: str,
        match_predicates: Dict[str, Any]
    ) -> Tuple[np.ndarray, List[int]]:
        matched_indices = []
        for idx, meta in enumerate(metadata_list):
            predicate_match = all(meta.get(k) == v for k, v in match_predicates.items())
            if predicate_match:
                matched_indices.append(idx)
        
        if not matched_indices:
            raise ValueError(
                f"No records found matching target predicates {match_predicates} "
                f"for entity '{target_entity}'. Homonym collision averted."
            )
        
        scoped_vectors = embeddings[matched_indices]
        centroid = np.mean(scoped_vectors, axis=0)
        norm = np.linalg.norm(centroid)
        if norm > 1e-12:
            centroid = centroid / norm
            
        return centroid, matched_indices

class UnlearningRollbackManager:
    """
    Manages transactional pre-state deltas and cryptographic undo logs,
    allowing deterministic reconstruction of scrubbed vectors.
    """
    def __init__(self, ttl_seconds: int = 604800):
        self.ttl_seconds = ttl_seconds
        self._ledger: Dict[str, Dict[str, Any]] = {}

    def stage_unlearning(
        self,
        embeddings: np.ndarray,
        target_indices: List[int],
        centroid: np.ndarray
    ) -> Tuple[np.ndarray, str]:
        c_norm = centroid / np.linalg.norm(centroid)
        deltas: Dict[int, np.ndarray] = {}
        scrubbed_embeddings = embeddings.copy()
        
        tx_data = f"{time.time()}_{len(target_indices)}_{np.sum(centroid):.6f}"
        tx_id = hashlib.sha256(tx_data.encode("utf-8")).hexdigest()[:16]
        
        for idx in target_indices:
            v = embeddings[idx]
            projection_component = float(np.dot(c_norm, v)) * c_norm
            deltas[idx] = projection_component.astype(np.float32)
            scrubbed_embeddings[idx] = v - projection_component
            
        self._ledger[tx_id] = {
            "deltas": deltas,
            "timestamp": time.time(),
            "indices": target_indices,
            "centroid_hash": hashlib.sha256(c_norm.tobytes()).hexdigest()
        }
        
        return scrubbed_embeddings, tx_id

    def rollback_transaction(
        self,
        current_embeddings: np.ndarray,
        tx_id: str
    ) -> np.ndarray:
        if tx_id not in self._ledger:
            raise KeyError(f"Transaction ID {tx_id} not found or expired in rollback ledger.")
        
        tx_entry = self._ledger[tx_id]
        if time.time() - tx_entry["timestamp"] > self.ttl_seconds:
            del self._ledger[tx_id]
            raise TimeoutError(f"Rollback window for transaction {tx_id} has expired.")
            
        restored_embeddings = current_embeddings.copy()
        for idx, delta in tx_entry["deltas"].items():
            restored_embeddings[idx] = restored_embeddings[idx] + delta
            
        del self._ledger[tx_id]
        return restored_embeddings

    def get_transaction_status(self, tx_id: str) -> Optional[Dict[str, Any]]:
        if tx_id not in self._ledger:
            return None
        entry = self._ledger[tx_id]
        return {
            "tx_id": tx_id,
            "records_affected": len(entry["indices"]),
            "timestamp": entry["timestamp"],
            "expires_in_seconds": max(0, self.ttl_seconds - (time.time() - entry["timestamp"])),
            "centroid_sha256": entry["centroid_hash"]
        }
