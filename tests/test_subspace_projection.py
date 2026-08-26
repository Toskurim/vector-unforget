"""
Tests for Subspace Projection Engine.
"""

from vector_unforget.subspace_projection import SubspaceProjector


def test_orthogonal_projection_single():
    projector = SubspaceProjector()
    target = [0.8, 0.6, 0.0]
    concept = [1.0, 0.0, 0.0]

    unlearned = projector.project_orthogonal(target, concept, normalize=True)
    assert abs(unlearned[0]) < 1e-5
    assert abs(unlearned[1] - 1.0) < 1e-5


def test_batch_matrix_projection():
    projector = SubspaceProjector()
    embeddings = [
        [0.8, 0.6, 0.0],
        [0.6, 0.8, 0.0],
        [0.0, 1.0, 0.0]
    ]
    concept = [1.0, 0.0, 0.0]

    unlearned_batch = projector.project_matrix_orthogonal(embeddings, concept, normalize=True)
    assert len(unlearned_batch) == 3
    for v in unlearned_batch:
        assert abs(v[0]) < 1e-5