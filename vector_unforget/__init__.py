"""
VectorUnforget: GDPR/CCPA PII Erasure Engine for Vector Databases.
Author: Toskurim
License: AGPLv3
"""

__version__ = "3.4.0"

from vector_unforget.engine import VectorUnforgetEngine
from vector_unforget.graph_resolver import PIIEntityGraph
from vector_unforget.subspace_projection import SubspaceProjector
from vector_unforget.verifier import ReverseRAGVerifier
from vector_unforget.hybrid_scrubber import HybridSearchScrubber

try:
    from vector_unforget.api.server import create_app
except ImportError:
    create_app = None

__all__ = [
    "__version__",
    "VectorUnforgetEngine",
    "PIIEntityGraph",
    "SubspaceProjector",
    "ReverseRAGVerifier",
    "HybridSearchScrubber",
    "create_app",
]
