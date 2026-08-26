# VectorUnforget - Development Roadmap

## Completed Milestones (v1.0.0 - v3.1.0)
- [x] **Core Engine**: Cascading PII detection via Regex & spaCy NER.
- [x] **Graph Resolver**: Transient multi-hop entity graph with decay weighting.
- [x] **Subspace Projector**: NumPy-based batch matrix orthogonal subspace projection.
- [x] **Vector DB Adapters**: Pinecone, Weaviate, LanceDB, Qdrant, Pgvector, ChromaDB.
- [x] **RAG Middleware**: Drop-in adapters for LangChain & LlamaIndex.
- [x] **Adversarial Verification**: Reverse RAG probe with Zero Residual Leakage scoring.
- [x] **Industrial Architecture**: PEP 517/621 packaging, GitHub Actions matrix CI/CD, dedicated `/tests` suite.

---

## Phase 10: v3.2.0 - Performance & Advanced Linear Algebra
- [ ] **10.1 GPU / CUDA Subspace Acceleration**
  - Implement optional backend execution via PyTorch / CuPy.
  - Zero-copy tensor projection for batch sizes > 100k vectors on VRAM.
  - Automated fallback to NumPy backend when CUDA devices are absent.
- [ ] **10.2 Multidimensional Concept Discovery (SVD / PCA)**
  - Automated subspace discovery using Singular Value Decomposition on semantic clusters.
  - Multi-rank concept erasure ($k$-dimensional hyperplane projection) for alias variations.
  - Orthogonality preservation and variance retention metrics calculation.

---

## Phase 11: v3.3.0 - Hybrid Search Erasure & New Ecosystem Adapters
- [ ] **11.1 Milvus Vector Database Adapter**
  - Distributed collection partition and entity purge implementation.
  - Batch scalar/vector deletion with consistency level configuration.
- [ ] **11.2 Elasticsearch & OpenSearch (k-NN) Adapter**
  - Dense vector field projection and doc-level deletion hooks.
- [ ] **11.3 Hybrid Index Synchronization**
  - Dual-phase unlearning: dense embedding subspace projection + sparse BM25 token scrubbing.
  - Prevention of keyword-based lexical leakage on unlearned semantic concepts.

---

## Phase 12: v3.4.0 - Enterprise Microservice Architecture
- [ ] **12.1 FastAPI High-Throughput REST Gateway**
  - Asynchronous endpoints: `POST /v1/unlearn/batch`, `POST /v1/graph/resolve`, `POST /v1/audit/verify`.
  - Pydantic v2 validation and structured JSON schema error handling.
- [ ] **12.2 Production Containerization & Deployment**
  - Multi-stage Docker build with CPU and GPU runtime profiles.
  - Helm chart / Kubernetes manifests for auto-scaling worker nodes.
  - Prometheus metrics instrumentation for latency and throughput monitoring.