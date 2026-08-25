"""
Semantic Subspace Projection (Vector Unlearning Engine) for VectorUnforget.
Author: Toskurim
License: AGPLv3
"""

from typing import List, Union
import math


class SubspaceProjector:
    """
    Implements mathematical subspace nullification and orthogonal projection
    for deep semantic vector unlearning without index retraining.
    """

    @staticmethod
    def dot_product(v1: List[float], v2: List[float]) -> float:
        """Computes the dot product of two vectors."""
        return sum(a * b for a, b in zip(v1, v2))

    @staticmethod
    def norm(v: List[float]) -> float:
        """Computes the Euclidean norm (L2) of a vector."""
        return math.sqrt(sum(a * a for a in v))

    @staticmethod
    def normalize(v: List[float]) -> List[float]:
        """Normalizes a vector to unit length."""
        n = SubspaceProjector.norm(v)
        if n == 0.0:
            return v
        return [a / n for a in v]

    @staticmethod
    def compute_centroid(vectors: List[List[float]]) -> List[float]:
        """Calculates the geometric centroid (average vector) of a set of embeddings."""
        if not vectors:
            return []
        dim = len(vectors[0])
        centroid = [0.0] * dim
        for vec in vectors:
            for i in range(dim):
                centroid[i] += vec[i]
        n = len(vectors)
        return SubspaceProjector.normalize([c / n for c in centroid])

    def project_orthogonal(
        self,
        target_vector: List[float],
        concept_vector: List[float],
    ) -> List[float]:
        """
        Projects `target_vector` onto the subspace orthogonal to `concept_vector`.
        Removes all directional components aligned with the forgotten concept:
        v_unlearned = v - (v . u) * u
        """
        concept_unit = self.normalize(concept_vector)
        dot = self.dot_product(target_vector, concept_unit)

        # Subtract projection along concept direction
        unlearned = [
            round(t - dot * c, 6)
            for t, c in zip(target_vector, concept_unit)
        ]
        return self.normalize(unlearned)

    def batch_unlearn_vectors(
        self,
        vectors: List[List[float]],
        concept_basis: Union[List[float], List[List[float]]],
    ) -> List[List[float]]:
        """
        Applies orthogonal projection across a collection of vectors.
        """
        if isinstance(concept_basis[0], list):
            concept_vector = self.compute_centroid(concept_basis)
        else:
            concept_vector = concept_basis

        return [
            self.project_orthogonal(v, concept_vector)
            for v in vectors
        ]