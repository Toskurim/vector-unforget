"""
VectorUnforget: GDPR/CCPA PII Erasure Engine for Vector Databases.
Author: Toskurim
License: AGPLv3
"""

__version__ = "3.3.0"

from vector_unforget.engine import VectorUnforgetEngine
from vector_unforget.graph_resolver import PIIEntityGraph
from vector_unforget.subspace_projection import SubspaceProjector
from vector_unforget.verifier import ReverseRAGVerifier
from vector_unforget.hybrid_scrubber import HybridSearchScrubber

__all__ = [
    "__version__",
    "VectorUnforgetEngine",
    "PIIEntityGraph",
    "SubspaceProjector",
    "ReverseRAGVerifier",
    "HybridSearchScrubber",
]