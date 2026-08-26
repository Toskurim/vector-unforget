"""
Subspace Projection Engine for Vector Unlearning.
Author: Toskurim
License: AGPLv3
"""

import math
from typing import List, Union

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False


class SubspaceProjector:
    """
    Applies orthogonal subspace projections to eliminate concept directions
    from vector embeddings without index retraining.
    """

    @staticmethod
    def _dot(v1: List[float], v2: List[float]) -> float:
        return sum(a * b for a, b in zip(v1, v2))

    @staticmethod
    def _norm(v: List[float]) -> float:
        return math.sqrt(sum(a * a for a in v))

    def project_orthogonal(
        self,
        target_vector: List[float],
        concept_vector: List[float],
        normalize: bool = True,
    ) -> List[float]:
        """
        Projects target_vector onto the orthogonal complement of concept_vector.
        Formula: v_unlearned = v - ((v . u) / (u . u)) * u
        """
        dot_product = self._dot(target_vector, concept_vector)
        concept_sq_norm = self._dot(concept_vector, concept_vector)

        if concept_sq_norm == 0.0:
            return list(target_vector)

        scalar = dot_product / concept_sq_norm
        projected = [t - scalar * c for t, c in zip(target_vector, concept_vector)]

        if normalize:
            norm_val = self._norm(projected)
            if norm_val > 0.0:
                projected = [p / norm_val for p in projected]

        return projected

    def project_matrix_orthogonal(
        self,
        embeddings: Union[List[List[float]], "np.ndarray"],
        concept_vector: Union[List[float], "np.ndarray"],
        normalize: bool = True,
    ) -> Union[List[List[float]], "np.ndarray"]:
        """
        High-throughput batch projection for large-scale embedding matrices.
        """
        if HAS_NUMPY:
            mat = np.asarray(embeddings, dtype=np.float32)
            u = np.asarray(concept_vector, dtype=np.float32)

            u_norm_sq = np.dot(u, u)
            if u_norm_sq == 0.0:
                return mat

            # Compute projections: P = X - (X @ u / u^T u)[:, None] * u
            projections = (np.matmul(mat, u) / u_norm_sq)[:, np.newaxis] * u
            unlearned = mat - projections

            if normalize:
                norms = np.linalg.norm(unlearned, axis=1, keepdims=True)
                norms[norms == 0.0] = 1.0
                unlearned = unlearned / norms

            return unlearned
        else:
            # Fallback a liste native
            return [
                self.project_orthogonal(v, list(concept_vector), normalize=normalize)
                for v in embeddings
            ]