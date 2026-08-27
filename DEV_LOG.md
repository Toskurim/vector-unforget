# VectorUnforget Development Log

## Version History

### [v3.7.0] - 2026-08-27
- **Interactive DPO Dashboard**: Added Streamlit web interface (`vector_unforget/dashboard.py`) for visual PII remediation, real-time graph inspection, and instant SHA-256 certificate download.
- **Test Suite**: 31/31 tests passing across core linear algebra, adapters, API microservice, compliance, metrics, and UI modules.

### [v3.6.0] - 2026-08-27
- **Prometheus Observability Gateway**: Added `GET /metrics` endpoint exporting vector scrubbing counters, SVD projection latency, and residual privacy leakage distribution.
- **MLOps Telemetry**: Integrated `MetricsTracker` directly into the FastAPI gateway pipeline.

### [v3.5.0] - 2026-08-27
- **Compliance & Cryptographic Audit**: Added `ComplianceCertificateGenerator` producing SHA-256 tamper-evident receipts for GDPR Art. 17 / CCPA compliance.
- **REST Certificate Endpoint**: Added `POST /v1/audit/certificate` for automated DPO receipt generation.

### [v3.4.0] - 2026-08-27
- **FastAPI Microservice Gateway**: Implemented high-throughput REST API with `/v1/unlearn/batch`, `/v1/graph/resolve`, and `/v1/audit/verify` endpoints.
- **Production Containerization**: Multi-stage lightweight Docker runtime.

### [v3.3.0] - 2026-08-26
- **Milvus & Elasticsearch Adapters**: Full coverage for distributed vector DBs and dense k-NN indices.
- **Hybrid Search Erasure**: Dual-phase sparse BM25 token scrubbing and dense subspace orthogonalization.

### [v3.2.0] - 2026-08-26
- **GPU Acceleration & SVD**: PyTorch CUDA integration and rank-$k$ concept subspace discovery.
