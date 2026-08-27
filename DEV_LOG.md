# VectorUnforget Development Log

## Version History

### [v3.5.0] - 2026-08-27
- **Compliance & Cryptographic Audit**: Added `ComplianceCertificateGenerator` producing SHA-256 tamper-evident receipts for GDPR Art. 17 / CCPA compliance.
- **REST Certificate Endpoint**: Added `POST /v1/audit/certificate` for automated DPO receipt generation.
- **Test Suite**: 28/28 tests passing across all core modules, adapters, microservice, and compliance reporting.

### [v3.4.0] - 2026-08-27
- **FastAPI Microservice Gateway**: Implemented high-throughput REST API with `/v1/unlearn/batch`, `/v1/graph/resolve`, and `/v1/audit/verify` endpoints.
- **Pydantic v2 Schemas**: Strict payload validation for array dimensions and numerical stability constraints.
- **Production Containerization**: Multi-stage lightweight Docker runtime.

### [v3.3.0] - 2026-08-26
- **Milvus & Elasticsearch Adapters**: Full coverage for distributed vector DBs and dense k-NN indices.
- **Hybrid Search Erasure**: Dual-phase sparse BM25 token scrubbing and dense subspace orthogonalization.

### [v3.2.0] - 2026-08-26
- **GPU Acceleration & SVD**: PyTorch CUDA integration and rank-$k$ concept subspace discovery.
