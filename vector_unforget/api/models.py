"""
Pydantic Schemas for VectorUnforget REST Gateway.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class UnlearnBatchRequest(BaseModel):
    embeddings: List[List[float]] = Field(..., description="List of N-dimensional vector embeddings")
    concept_vector: List[float] = Field(..., description="Target sensitive concept vector")
    normalize: bool = Field(default=True, description="L2-normalize resulting orthogonal vectors")


class UnlearnBatchResponse(BaseModel):
    status: str
    unlearned_embeddings: List[List[float]]
    vector_count: int


class GraphResolveRequest(BaseModel):
    primary_entity: str = Field(..., description="Primary PII identifier to resolve")
    max_hops: int = Field(default=2, ge=1, le=5, description="Maximum graph traversal depth")
    decay_factor: float = Field(default=0.8, gt=0.0, le=1.0, description="Confidence decay per hop")


class GraphResolveResponse(BaseModel):
    status: str
    primary_entity: str
    resolved_entities: List[Dict[str, Any]]
    total_nodes_erased: int


class AuditVerifyRequest(BaseModel):
    query_vector: List[float] = Field(..., description="Probe vector matching sensitive topic")
    retrieved_vectors: List[List[float]] = Field(..., description="Candidate vectors from RAG search")
    threshold: float = Field(default=0.15, description="Cosine similarity threshold for leakage flag")


class AuditVerifyResponse(BaseModel):
    status: str
    leakage_score: float
    max_similarity: float
    passed: bool


class CertificateRequest(BaseModel):
    request_id: str = Field(..., description="Unique compliance audit ticket ID")
    entity_identifier: str = Field(..., description="PII Entity identifier")
    unlearned_vector_count: int = Field(..., ge=0)
    pre_leakage_score: float = Field(..., ge=0.0)
    post_leakage_score: float = Field(..., ge=0.0)
    scrubbed_terms: Optional[List[str]] = Field(default_factory=list)
    regulation: str = Field(default="GDPR_Art_17")


class CertificateResponse(BaseModel):
    status: str
    certificate: Dict[str, Any]
