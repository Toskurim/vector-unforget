import numpy as np
import pytest
from vector_unforget.subspace_projection import SubspaceProjector, TORCH_AVAILABLE


def test_numpy_batch_projection_orthogonality():
    projector = SubspaceProjector(device="cpu")

    embeddings = np.array([
        [1.0, 1.0, 0.0],
        [0.5, 0.5, 0.5],
        [0.0, 2.0, 0.0]
    ], dtype=np.float32)

    concept_vector = np.array([1.0, 0.0, 0.0], dtype=np.float32)

    unlearned = projector.project_matrix_orthogonal(
        embeddings, concept_vector, normalize=True, backend="numpy"
    )

    for row in unlearned:
        dot_product = np.dot(row, concept_vector)
        assert abs(dot_product) < 1e-6
        assert abs(np.linalg.norm(row) - 1.0) < 1e-6


@pytest.mark.skipif(not TORCH_AVAILABLE, reason="PyTorch is not installed")
def test_torch_cpu_backend_equivalence():
    projector = SubspaceProjector()

    embeddings = np.random.randn(100, 64).astype(np.float32)
    concept_vector = np.random.randn(64).astype(np.float32)

    res_numpy = projector.project_matrix_orthogonal(embeddings, concept_vector, normalize=True, backend="numpy")
    res_torch = projector.project_matrix_orthogonal(embeddings, concept_vector, normalize=True, backend="torch_cpu")

    np.testing.assert_allclose(res_numpy, res_torch, rtol=1e-5, atol=1e-5)


def test_svd_multisubspace_projection():
    projector = SubspaceProjector(device="cpu")

    concept_cluster = np.random.randn(5, 8).astype(np.float32)
    basis, _ = projector.compute_concept_subspace(concept_cluster, rank=2)
    assert basis.shape == (2, 8)

    np.testing.assert_allclose(np.dot(basis[0], basis[1]), 0.0, atol=1e-5)
    np.testing.assert_allclose(np.linalg.norm(basis[0]), 1.0, atol=1e-5)
    np.testing.assert_allclose(np.linalg.norm(basis[1]), 1.0, atol=1e-5)

    embeddings = np.random.randn(20, 8).astype(np.float32)
    unlearned = projector.project_matrix_multisubspace(embeddings, basis, normalize=True)

    for row in unlearned:
        assert abs(np.dot(row, basis[0])) < 1e-5
        assert abs(np.dot(row, basis[1])) < 1e-5
        assert abs(np.linalg.norm(row) - 1.0) < 1e-5