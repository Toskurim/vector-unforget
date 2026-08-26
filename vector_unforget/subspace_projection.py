"""
Subspace Projection Engine for VectorUnforget.
Provides orthogonal subspace projection for vector unlearning with CPU (NumPy) and GPU (PyTorch/CUDA) support.
"""

from typing import Optional, Union, Tuple
import numpy as np

# Optional PyTorch detection for GPU acceleration
try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


class SubspaceProjector:
    """
    High-throughput engine to project vector embeddings onto orthogonal complements
    of sensitive concept subspaces, preventing semantic leakage.
    """

    def __init__(self, device: str = "auto"):
        self.device = self._resolve_device(device)

    def _resolve_device(self, device: str) -> str:
        if device == "cuda":
            if not TORCH_AVAILABLE or not torch.cuda.is_available():
                raise RuntimeError("CUDA execution requested but PyTorch or CUDA GPU is not available.")
            return "cuda"
        elif device == "auto":
            if TORCH_AVAILABLE and torch.cuda.is_available():
                return "cuda"
            return "cpu"
        return "cpu"

    def compute_concept_subspace(
        self,
        concept_embeddings: np.ndarray,
        rank: int = 1,
        energy_threshold: Optional[float] = None
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Extract the dominant orthonormal basis vectors spanning a concept subspace via SVD.
        
        Args:
            concept_embeddings: (M, D) array of embedding variations of the same concept.
            rank: Target subspace dimension (k).
            energy_threshold: Optional variance threshold (0.0 to 1.0) to dynamically select k.
            
        Returns:
            basis: (k, D) orthonormal basis matrix.
            singular_values: singular values representing energy per dimension.
        """
        X = np.asarray(concept_embeddings, dtype=np.float32)
        if X.ndim == 1:
            X = X.reshape(1, -1)

        X_centered = X - np.mean(X, axis=0, keepdims=True)
        _, S, Vt = np.linalg.svd(X_centered, full_matrices=False)

        if energy_threshold is not None:
            total_energy = np.sum(S ** 2)
            if total_energy > 0:
                cumulative_energy = np.cumsum(S ** 2) / total_energy
                rank = int(np.searchsorted(cumulative_energy, energy_threshold) + 1)
                rank = max(1, min(rank, Vt.shape[0]))

        k = max(1, min(rank, Vt.shape[0]))
        basis = Vt[:k, :]
        return basis, S[:k]

    def project_matrix_multisubspace(
        self,
        embeddings: np.ndarray,
        subspace_basis: np.ndarray,
        normalize: bool = True,
        eps: float = 1e-12
    ) -> np.ndarray:
        """
        Project an embedding matrix (N, D) onto the orthogonal complement of a k-dimensional subspace (k, D).
        Formula: X_unlearned = X - X @ Basis.T @ Basis
        """
        X = np.asarray(embeddings, dtype=np.float32)
        B = np.asarray(subspace_basis, dtype=np.float32)

        if B.ndim == 1:
            B = B.reshape(1, -1)

        projection = np.dot(np.dot(X, B.T), B)
        X_unlearned = X - projection

        if normalize:
            norms = np.linalg.norm(X_unlearned, axis=1, keepdims=True)
            norms = np.maximum(norms, eps)
            X_unlearned = X_unlearned / norms

        return X_unlearned

    def project_orthogonal(
        self,
        vector: np.ndarray,
        concept_vector: np.ndarray,
        normalize: bool = True,
        eps: float = 1e-12
    ) -> np.ndarray:
        v = np.asarray(vector, dtype=np.float32)
        c = np.asarray(concept_vector, dtype=np.float32)

        dot_cc = float(np.dot(c, c))
        if dot_cc < eps:
            return v

        c_norm_sq = dot_cc
        projection = (np.dot(v, c) / c_norm_sq) * c
        v_unlearned = v - projection

        if normalize:
            norm = np.linalg.norm(v_unlearned)
            if norm > eps:
                v_unlearned = v_unlearned / norm

        return v_unlearned

    def project_matrix_orthogonal(
        self,
        embeddings: Union[np.ndarray, "torch.Tensor"],
        concept_vector: Union[np.ndarray, "torch.Tensor"],
        normalize: bool = True,
        eps: float = 1e-12,
        backend: Optional[str] = None
    ) -> Union[np.ndarray, "torch.Tensor"]:
        target_backend = backend or ("torch_cuda" if self.device == "cuda" else "numpy")

        if "torch" in target_backend:
            if not TORCH_AVAILABLE:
                raise ImportError("PyTorch is required for torch backend execution.")
            return self._project_torch(embeddings, concept_vector, normalize, eps, use_cuda=("cuda" in target_backend))
        else:
            return self._project_numpy(embeddings, concept_vector, normalize, eps)

    def _project_numpy(
        self,
        embeddings: np.ndarray,
        concept_vector: np.ndarray,
        normalize: bool,
        eps: float
    ) -> np.ndarray:
        X = np.asarray(embeddings, dtype=np.float32)
        c = np.asarray(concept_vector, dtype=np.float32)

        dot_cc = float(np.dot(c, c))
        if dot_cc < eps:
            return X

        scales = (np.dot(X, c) / dot_cc)[:, np.newaxis]
        X_proj = scales * c
        X_unlearned = X - X_proj

        if normalize:
            norms = np.linalg.norm(X_unlearned, axis=1, keepdims=True)
            norms = np.maximum(norms, eps)
            X_unlearned = X_unlearned / norms

        return X_unlearned

    def _project_torch(
        self,
        embeddings: Union[np.ndarray, "torch.Tensor"],
        concept_vector: Union[np.ndarray, "torch.Tensor"],
        normalize: bool,
        eps: float,
        use_cuda: bool
    ) -> np.ndarray:
        device = "cuda" if (use_cuda and torch.cuda.is_available()) else "cpu"

        if isinstance(embeddings, np.ndarray):
            t_X = torch.from_numpy(embeddings).float().to(device)
        else:
            t_X = embeddings.float().to(device)

        if isinstance(concept_vector, np.ndarray):
            t_c = torch.from_numpy(concept_vector).float().to(device)
        else:
            t_c = concept_vector.float().to(device)

        dot_cc = torch.dot(t_c, t_c).item()
        if dot_cc < eps:
            return t_X.cpu().numpy() if isinstance(embeddings, np.ndarray) else t_X

        scales = (torch.matmul(t_X, t_c) / dot_cc).unsqueeze(1)
        t_unlearned = t_X - (scales * t_c)

        if normalize:
            norms = torch.norm(t_unlearned, dim=1, keepdim=True).clamp(min=eps)
            t_unlearned = t_unlearned / norms

        if isinstance(embeddings, np.ndarray):
            return t_unlearned.cpu().numpy()
        return t_unlearned