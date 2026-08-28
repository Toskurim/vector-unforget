import numpy as np
import pytest
from vector_unforget.enterprise import MetadataScopedScrubber, UnlearningRollbackManager

def test_homonym_disambiguation():
    scrubber = MetadataScopedScrubber(embedding_dim=4)
    embeddings = np.array([
        [1.0, 0.0, 0.0, 0.0],
        [0.9, 0.1, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0]
    ])
    metadata = [
        {"name": "Mario Rossi", "user_id": "user_101", "org": "Finance"},
        {"name": "Mario Rossi", "user_id": "user_101", "org": "Finance"},
        {"name": "Mario Rossi", "user_id": "user_999", "org": "Legal"}
    ]
    centroid, target_indices = scrubber.filter_and_extract_centroid(
        embeddings=embeddings,
        metadata_list=metadata,
        target_entity="Mario Rossi",
        match_predicates={"user_id": "user_101"}
    )
    assert target_indices == [0, 1]
    assert 2 not in target_indices

def test_lossless_rollback_cycle():
    rollback_mgr = UnlearningRollbackManager(ttl_seconds=3600)
    np.random.seed(42)
    original_vectors = np.random.randn(50, 128).astype(np.float32)
    original_vectors /= np.linalg.norm(original_vectors, axis=1, keepdims=True)
    
    target_indices = [5, 12, 27]
    sensitive_centroid = np.mean(original_vectors[target_indices], axis=0)
    sensitive_centroid /= np.linalg.norm(sensitive_centroid)
    
    scrubbed_vectors, tx_id = rollback_mgr.stage_unlearning(
        embeddings=original_vectors,
        target_indices=target_indices,
        centroid=sensitive_centroid
    )
    
    for idx in target_indices:
        cos_sim = np.dot(scrubbed_vectors[idx], sensitive_centroid)
        assert abs(cos_sim) < 1e-6
        
    restored_vectors = rollback_mgr.rollback_transaction(
        current_embeddings=scrubbed_vectors,
        tx_id=tx_id
    )
    
    np.testing.assert_allclose(original_vectors, restored_vectors, rtol=1e-5, atol=1e-5)
