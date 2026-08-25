"""
VectorUnforget: GDPR/CCPA Right-to-be-Forgotten Engine for Vector Databases.
Author: Toskurim
License: AGPLv3
"""

from .engine import VectorUnforgetEngine
from .verifier import ReverseRAGVerifier
from .graph_resolver import PIIEntityGraph
from .subspace_projection import SubspaceProjector

# Re-export adapters
from .adapters.base import BaseVectorAdapter
from .adapters.chroma import ChromaAdapter
from .adapters.pgvector import PgvectorAdapter
from .adapters.qdrant import QdrantAdapter
from .adapters.pinecone import PineconeAdapter
from .adapters.weaviate import WeaviateAdapter

# Re-export middleware
from .middleware.langchain_retriever import VectorUnforgetRetriever
from .middleware.llamaindex_processor import VectorUnforgetNodePostprocessor

try:
    from .auditor import Auditor
except ImportError:
    try:
        from .auditor import AuditLogger as Auditor
    except ImportError:
        Auditor = None

__all__ = [
    "VectorUnforgetEngine",
    "ReverseRAGVerifier",
    "PIIEntityGraph",
    "SubspaceProjector",
    "Auditor",
    "BaseVectorAdapter",
    "ChromaAdapter",
    "PgvectorAdapter",
    "QdrantAdapter",
    "PineconeAdapter",
    "WeaviateAdapter",
    "VectorUnforgetRetriever",
    "VectorUnforgetNodePostprocessor",
]