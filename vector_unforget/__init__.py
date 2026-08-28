"""
VectorUnforget - Enterprise AI Middleware for Verifiable PII Oblivion & Vector Unlearning.
"""

__version__ = "4.2.0"

from vector_unforget.subspace_projection import SubspaceProjector
from vector_unforget.graph_resolver import PIIEntityGraph
from vector_unforget.compliance import ComplianceCertificateGenerator
from vector_unforget.hybrid_scrubber import HybridSearchScrubber
from vector_unforget.oblivion import OblivionExtractor

try:
    from vector_unforget.verifier import AdversarialLeakageVerifier as UnlearningVerifier
except ImportError:
    try:
        from vector_unforget.verifier import UnlearningVerifier
    except ImportError:
        UnlearningVerifier = None

HybridScrubber = HybridSearchScrubber

__all__ = [
    "SubspaceProjector",
    "PIIEntityGraph",
    "ComplianceCertificateGenerator",
    "UnlearningVerifier",
    "HybridScrubber",
    "HybridSearchScrubber",
    "OblivionExtractor",
]

