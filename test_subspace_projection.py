"""
Test Suite: Semantic Subspace Projection (Vector Unlearning).
Author: Toskurim
"""

from vector_unforget.subspace_projection import SubspaceProjector
import math


def test_orthogonal_projection_nullifies_concept():
    projector = SubspaceProjector()

    # Concept vector to forget (along X axis)
    concept = [1.0, 0.0, 0.0]

    # Target vector containing both sensitive and non-sensitive dimensions
    target = [0.8, 0.6, 0.0]  # Mixed vector

    # Perform orthogonal unlearning
    unlearned = projector.project_orthogonal(target, concept)

    # The projection onto concept must now be 0 (orthogonality condition)
    dot_remaining = projector.dot_product(unlearned, concept)
    assert abs(dot_remaining) < 1e-5

    # Non-sensitive dimension (Y axis) should be preserved and normalized
    assert unlearned[0] == 0.0
    assert math.isclose(unlearned[1], 1.0, rel_tol=1e-5)


def test_batch_unlearn_with_centroid():
    projector = SubspaceProjector()

    concept_samples = [
        [1.0, 0.1, 0.0],
        [0.9, -0.1, 0.0],
    ]

    target_vectors = [
        [0.707, 0.707, 0.0],
        [0.5, 0.0, 0.866],
    ]

    unlearned_batch = projector.batch_unlearn_vectors(target_vectors, concept_samples)

    assert len(unlearned_batch) == 2
    for vec in unlearned_batch:
        # Check that norm is valid
        assert math.isclose(projector.norm(vec), 1.0, rel_tol=1e-4)


if __name__ == "__main__":
    test_orthogonal_projection_nullifies_concept()
    test_batch_unlearn_with_centroid()
    print("✅ Semantic Subspace Projection tests passed successfully!")