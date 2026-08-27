from vector_unforget.adapters.base import BaseVectorAdapter, BaseVectorStoreAdapter

try:
    from vector_unforget.adapters.pinecone_adapter import PineconeAdapter
except ImportError:
    from vector_unforget.adapters.pinecone import PineconeAdapter

try:
    from vector_unforget.adapters.weaviate_adapter import WeaviateAdapter
except ImportError:
    from vector_unforget.adapters.weaviate import WeaviateAdapter

try:
    from vector_unforget.adapters.lancedb_adapter import LanceDBAdapter
except ImportError:
    LanceDBAdapter = None

try:
    from vector_unforget.adapters.milvus_adapter import MilvusAdapter
except ImportError:
    MilvusAdapter = None

try:
    from vector_unforget.adapters.elasticsearch_adapter import ElasticsearchAdapter
except ImportError:
    ElasticsearchAdapter = None

try:
    from vector_unforget.adapters.qdrant_adapter import QdrantAdapter
except ImportError:
    QdrantAdapter = None

try:
    from vector_unforget.adapters.chroma_adapter import ChromaAdapter
except ImportError:
    ChromaAdapter = None

__all__ = [
    'BaseVectorAdapter',
    'BaseVectorStoreAdapter',
    'PineconeAdapter',
    'WeaviateAdapter',
    'LanceDBAdapter',
    'MilvusAdapter',
    'ElasticsearchAdapter',
    'QdrantAdapter',
    'ChromaAdapter',
]
