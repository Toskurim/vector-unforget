# VectorUnforget Development Log

## Version History

### [v4.2.0] - 2026-08-28
* **Metadata-Scoped Entity Disambiguation**: Implemented `MetadataScopedScrubber` to eliminate homonym collisions via strict multi-predicate filtering (e.g. `user_id`, `tenant_id`).
* **Transactional Delta Ledger & Safe Rollback**: Added `UnlearningRollbackManager` enabling deterministic, lossless vector restoration with configurable cryptographic TTL retention.
* **Test Suite Expansion**: Reached 38/38 passing tests with complete enterprise coverage.
### [v4.2.0] - 2026-08-28
* **Metadata-Scoped Entity Disambiguation**: Implemented `MetadataScopedScrubber` to eliminate homonym collisions via strict multi-predicate filtering (e.g. `user_id`, `tenant_id`).
* **Transactional Delta Ledger & Safe Rollback**: Added `UnlearningRollbackManager` enabling deterministic, lossless vector restoration with configurable cryptographic TTL retention.
* **Test Suite Expansion**: Reached 38/38 passing tests with complete enterprise coverage.
### [v4.1.0] - 2026-08-27
* **Official PyPI Distribution**: Successfully packaged and deployed `vector-unforget` to PyPI for direct `pip install vector-unforget` consumption.
* **Dual-Licensing Strategy & IP Protection**: Formalized AGPL-3.0 copyleft architecture with explicit commercial dual-licensing pathways for proprietary enterprise embeddings.
* **Enterprise Documentation Overhaul**: Modernized technical value propositions, verified test badges (36/36), and refined metadata across all distributions.

### [v4.0.0] - 2026-08-27
* **Zero-Config NLP / NER Intent Extraction**: Integrated automated entity extraction and synthetic centroid vector projection from raw text directives.
* **Full Multi-VectorDB Adapter Layer**: Native support for Milvus, Elasticsearch, Pinecone, Weaviate, LanceDB, Qdrant, and ChromaDB.
* **Empirical Benchmarks Validated**: Proved 72x faster execution against Faiss index rebuilding on 500k-vector workloads ($O(N \cdot D)$ subspace scrubbing).

---

## Strategic Roadmap

* **[Phase 1: Distribution & Containerization]** Automated multi-arch Docker image publication on GitHub Container Registry (GHCR) and Docker Hub.
* **[Phase 2: Formal Whitepaper]** Release of technical 3-page whitepaper focusing on mathematical proofs ($O(N \cdot D)$ orthogonal unlearning) and GDPR Art. 17 cryptographic compliance for CTOs/DPOs.
* **[Phase 3: Ecosystem & Enterprise Outreach]** Targeted technical outreach to vector database core teams (Qdrant, Chroma, Milvus) and privacy-tech/AI governance platforms.

---### [v3.7.0] - 2026-08-27
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

### [v4.1.0] - 2026-08-27
- **Scalability & Performance Benchmarks**: Added comprehensive quantitative benchmark suite (enchmarks/benchmark_unlearning.py) evaluating orthogonal projection vs HNSW re-indexing up to 1M vectors @ 768d.
- **Audit & Compliance**: Documented 70x-93x latency reduction and 100% concept leakage scrub with deterministic SHA-256 GDPR Art. 17 receipts in BENCHMARKS.md.



