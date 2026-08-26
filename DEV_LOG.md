# VectorUnforget Development Log

## Version History

### [v3.3.0] - 2026-08-26
- **Milvus Adapter**: Native distributed entity deletion via primary key and scalar expressions.
- **Elasticsearch & OpenSearch Adapter**: Full support for index-level document scrubbing and k-NN dense vector erasure.
- **Hybrid Search Erasure**: Introduced `HybridSearchScrubber` for dual-phase dense embedding orthogonal projection and sparse BM25 lexical token sanitization.
- **Test Suite**: 23/23 tests passing across core linear algebra, adapters, and middleware.

### [v3.2.0] - 2026-08-26
- **GPU Acceleration**: Integrated PyTorch/CUDA execution into `SubspaceProjector` with transparent fallback to NumPy.
- **Multidimensional Concept Discovery**: Implemented Singular Value Decomposition (SVD) for extracting rank-$k$ orthonormal bases from semantic concept clusters.
- **Matrix Hyperplane Projection**: Added `project_matrix_multisubspace` for batch orthogonalization against multidimensional concept directions.

---

## Active Roadmap

### Phase 12: v3.4.0 - Enterprise Microservice Architecture
- [ ] **12.1 FastAPI High-Throughput REST Gateway**
  - Asynchronous endpoints: `/v1/unlearn/batch`, `/v1/graph/resolve`, `/v1/audit/verify`.
  - Pydantic v2 schemas and validation models.
- [ ] **12.2 Production Containerization & Deployment**
  - Multi-stage Docker build (CPU & CUDA profiles).
  - Helm charts and Prometheus metrics instrumentation.