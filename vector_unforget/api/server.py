"""
FastAPI Server Application for VectorUnforget REST Gateway.
"""

from typing import Dict, Any
import numpy as np
from fastapi import FastAPI, HTTPException, status

from vector_unforget import __version__
from vector_unforget.subspace_projection import SubspaceProjector
from vector_unforget.graph_resolver import PIIEntityGraph
from vector_unforget.api.models import (
    UnlearnBatchRequest,
    UnlearnBatchResponse,
    GraphResolveRequest,
    GraphResolveResponse,
    AuditVerifyRequest,
    AuditVerifyResponse,
)


def create_app() -> FastAPI:
    app = FastAPI(
        title="VectorUnforget API",
        version=__version__,
        description="High-Throughput Vector Unlearning and Cascading PII Erasure Microservice",
    )

    projector = SubspaceProjector(device="auto")

    @app.get("/health", tags=["System"])
    async def health_check() -> Dict[str, Any]:
        return {"status": "healthy", "version": __version__, "device": projector.device}

    @app.post("/v1/unlearn/batch", response_model=UnlearnBatchResponse, tags=["Unlearning"])
    async def unlearn_batch(payload: UnlearnBatchRequest) -> UnlearnBatchResponse:
        if not payload.embeddings or not payload.concept_vector:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Embeddings list and concept_vector cannot be empty."
            )

        try:
            arr_embeddings = np.array(payload.embeddings, dtype=np.float32)
            arr_concept = np.array(payload.concept_vector, dtype=np.float32)

            if arr_embeddings.shape[1] != arr_concept.shape[0]:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Dimension mismatch: embeddings dimension {arr_embeddings.shape[1]} != concept dimension {arr_concept.shape[0]}"
                )

            unlearned = projector.project_matrix_orthogonal(
                embeddings=arr_embeddings,
                concept_vector=arr_concept,
                normalize=payload.normalize
            )

            return UnlearnBatchResponse(
                status="success",
                unlearned_embeddings=unlearned.tolist(),
                vector_count=len(payload.embeddings)
            )
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    @app.post("/v1/graph/resolve", response_model=GraphResolveResponse, tags=["Graph"])
    async def resolve_graph(payload: GraphResolveRequest) -> GraphResolveResponse:
        try:
            graph = PIIEntityGraph(decay_factor=payload.decay_factor)
            resolved = graph.resolve_cascading_entities(payload.primary_entity, max_hops=payload.max_hops)
            formatted = [{"entity": entity, "confidence": conf} for entity, conf in resolved.items()]

            return GraphResolveResponse(
                status="success",
                primary_entity=payload.primary_entity,
                resolved_entities=formatted,
                total_nodes_erased=len(formatted)
            )
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    @app.post("/v1/audit/verify", response_model=AuditVerifyResponse, tags=["Audit"])
    async def verify_audit(payload: AuditVerifyRequest) -> AuditVerifyResponse:
        try:
            if not payload.retrieved_vectors:
                return AuditVerifyResponse(
                    status="success",
                    leakage_score=0.0,
                    max_similarity=0.0,
                    passed=True
                )

            q = np.array(payload.query_vector, dtype=np.float32)
            q_norm = np.linalg.norm(q)
            if q_norm > 1e-9:
                q = q / q_norm

            sims = []
            for v in payload.retrieved_vectors:
                v_arr = np.array(v, dtype=np.float32)
                v_norm = np.linalg.norm(v_arr)
                if v_norm > 1e-9:
                    v_arr = v_arr / v_norm
                sims.append(float(np.dot(q, v_arr)))

            max_sim = max(sims) if sims else 0.0
            passed = max_sim < payload.threshold

            return AuditVerifyResponse(
                status="success",
                leakage_score=max(0.0, max_sim),
                max_similarity=max_sim,
                passed=passed
            )
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return app
