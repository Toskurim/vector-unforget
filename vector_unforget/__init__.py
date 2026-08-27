"""
VectorUnforget - Enterprise AI Middleware for Verifiable PII Oblivion & Vector Unlearning.
"""

__version__ = "4.1.0"

from vector_unforget.subspace_projection import SubspaceProjector
from vector_unforget.graph_resolver import PIIEntityGraph
from vector_unforget.compliance import ComplianceCertificateGenerator
from vector_unforget.verifier import UnlearningVerifier
from vector_unforget.hybrid_scrubber import HybridScrubber
from vector_unforget.oblivion import OblivionExtractor

__all__ = [
    "SubspaceProjector",
    "PIIEntityGraph",
    "ComplianceCertificateGenerator",
    "UnlearningVerifier",
    "HybridScrubber",
    "OblivionExtractor",
]
