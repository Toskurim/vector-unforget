"""
Hybrid Search Erasure Module for VectorUnforget.
Coordinates dense embedding subspace projection and sparse BM25 token scrubbing.
"""

from typing import List, Dict, Any, Set, Optional
import re
import numpy as np
from vector_unforget.subspace_projection import SubspaceProjector


class HybridSearchScrubber:
    """
    Coordinates simultaneous erasure across dense vector spaces and sparse lexical indices.
    """

    def __init__(self, subspace_projector: Optional[SubspaceProjector] = None):
        self.projector = subspace_projector or SubspaceProjector()

    def scrub_text_tokens(self, text: str, sensitive_terms: Set[str], replacement: str = "[REDACTED]") -> str:
        """
        Sanitize raw text by replacing lexical tokens to prevent BM25 sparse keyword leakage.
        """
        if not text or not sensitive_terms:
            return text

        scrubbed = text
        for term in sensitive_terms:
            if not term.strip():
                continue
            pattern = re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE)
            scrubbed = pattern.sub(replacement, scrubbed)

        return scrubbed

    def process_hybrid_document(
        self,
        doc_text: str,
        embedding: np.ndarray,
        concept_vector: np.ndarray,
        sensitive_terms: Set[str],
        normalize: bool = True
    ) -> Dict[str, Any]:
        """
        Execute dual-phase scrubbing on a document record:
        1. Dense phase: Orthogonal subspace projection on embedding vector.
        2. Sparse phase: Lexical token sanitization on raw text.
        """
        unlearned_vec = self.projector.project_orthogonal(
            vector=embedding,
            concept_vector=concept_vector,
            normalize=normalize
        )

        sanitized_text = self.scrub_text_tokens(
            text=doc_text,
            sensitive_terms=sensitive_terms
        )

        return {
            "sanitized_text": sanitized_text,
            "unlearned_vector": unlearned_vec,
            "terms_scrubbed": list(sensitive_terms)
        }