"""
VectorUnforget: GDPR/CCPA PII Erasure Engine for Vector Databases.
Author: Toskurim
License: AGPLv3
"""

__version__ = "4.0.0"

from vector_unforget.engine import VectorUnforgetEngine
from vector_unforget.graph_resolver import PIIEntityGraph
from vector_unforget.subspace_projection import SubspaceProjector
from vector_unforget.verifier import ReverseRAGVerifier
from vector_unforget.hybrid_scrubber import HybridSearchScrubber
from vector_unforget.compliance import ComplianceCertificateGenerator
from vector_unforget.metrics import metrics_collector

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
    "ComplianceCertificateGenerator",
    "metrics_collector",
    "create_app",
]
