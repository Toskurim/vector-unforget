# VectorUnforget

[![Version](https://img.shields.io/badge/version-4.1.0-blue.svg)](https://github.com/Toskurim/vector-unforget)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-blue)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-36%2F36%20passing-brightgreen.svg)](https://github.com/Toskurim/vector-unforget)
[![Observability](https://img.shields.io/badge/observability-Prometheus%20ready-orange.svg)](https://prometheus.io/)

**VectorUnforget** is an enterprise-grade AI middleware engine designed for verifiable PII erasure, concept unlearning, and GDPR (Art. 17) / CCPA compliance across vector databases and RAG pipelines.

---

## Core Capabilities

- **Subspace Orthogonal Projection**: Deterministic concept unlearning using SVD and PyTorch CUDA/CPU acceleration without full index re-indexing.
- **Cascading PII Entity Graph**: Multi-hop entity resolution with exponential confidence decay to erase connected identities.
- **Hybrid Search Scrubbing**: Unified dense vector orthogonalization combined with sparse lexical BM25 token redaction.
- **Production Vector DB Adapters**: Native drivers for **Milvus**, **Elasticsearch / OpenSearch**, **Pinecone**, **Weaviate**, and **LanceDB**.
- **RAG Framework Integrations**: Native middleware for **LangChain** (`VectorUnforgetRetriever`) and **LlamaIndex** (`VectorUnforgetNodePostprocessor`).
- **Cryptographic Audit Receipts**: Tamper-evident **SHA-256** erasure certificates verifying *Zero Residual Leakage* for Data Protection Officers.
- **MLOps Telemetry**: Built-in Prometheus exposition endpoint (`GET /metrics`) tracking unlearning throughput, SVD latency, and leakage distribution.
- **Interactive DPO Console**: Streamlit-based web interface for live PII remediation, graph traversal preview, and instant compliance certificate export.

---

## Quickstart

### 1. Installation

```bash
pip install vector-unforget
```

### 2. Python SDK Example

```python
from vector_unforget.subspace_projection import SubspaceProjector
from vector_unforget.compliance import ComplianceCertificateGenerator
import numpy as np

projector = SubspaceProjector(device="auto")
embeddings = np.random.randn(100, 768).astype(np.float32)
sensitive_concept = np.random.randn(768).astype(np.float32)

unlearned = projector.project_matrix_orthogonal(embeddings, sensitive_concept, normalize=True)

cert_gen = ComplianceCertificateGenerator()
cert = cert_gen.generate_certificate(
    request_id="REQ-GDPR-001",
    entity_identifier="user_9941",
    unlearned_vector_count=100,
    pre_unlearning_leakage=0.85,
    post_unlearning_leakage=0.002,
    regulation="GDPR_Art_17"
)
print("Receipt SHA-256:", cert["cryptographic_hash_sha256"])
```

### 3. Running the REST Gateway

```bash
uvicorn vector_unforget.api.server:create_app --factory --host 0.0.0.0 --port 8000
```

### 4. Running the Interactive DPO Console

```bash
streamlit run vector_unforget/dashboard.py
```

---

## REST Endpoints Overview

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Service status and compute device info |
| `GET` | `/metrics` | Prometheus metrics for MLOps observability |
| `POST` | `/v1/unlearn/batch` | High-throughput batch vector orthogonal projection |
| `POST` | `/v1/graph/resolve` | Cascading multi-hop PII entity discovery |
| `POST` | `/v1/audit/verify` | Adversarial probe vector leakage verification |
| `POST` | `/v1/audit/certificate` | Generate signed SHA-256 GDPR/CCPA erasure receipts |

---

## License

Distributed under the **AGPLv3** License. See `LICENSE` for details.

## ⚡ Empirical Performance & Scalability Benchmarks

VectorUnforget replaces expensive vector database re-indexing with **(N \cdot D)$ Orthogonal Subspace Projection**, drastically cutting GDPR Art. 17 right-to-erasure latency while ensuring complete mathematical mitigation of target concept leakage.

### Measured Results (Host CPU vs Native Faiss C++ HNSW)

All values are **physically measured wall-clock times** across dense 768-dimensional float32 vector collections.

| Vectors ($) | Latency (VU Projection) | Baseline (Faiss C++ HNSWFlat) | Empirical Speedup | Memory Peak (MB) | Residual Concept Leakage | Cryptographic Audit Proof |
|---|---|---|---|---|---|---|
| **10,000** | **31.12 ms** | 336.14 ms | **10.8x** | 58.74 MB | -0.0 (100% Scrubbed) | SHA-256 Verified |
| **50,000** | **146.73 ms** | 3.41 s | **23.2x** | 293.57 MB | -0.0 (100% Scrubbed) | SHA-256 Verified |
| **100,000** | **304.28 ms** | 12.52 s | **41.1x** | 587.11 MB | -0.0 (100% Scrubbed) | SHA-256 Verified |
| **250,000** | **773.19 ms** | 45.91 s | **59.4x** | 1,467.74 MB | -0.0 (100% Scrubbed) | SHA-256 Verified |
| **500,000** | **1.52 s** | 109.16 s (~1.8 min) | **72.0x** | 2,935.44 MB | -0.0 (100% Scrubbed) | SHA-256 Verified |

> 📊 **Full Methodology & Reproduction**: See [BENCHMARKS.md](BENCHMARKS.md) for execution parameters, memory profiling, and test scripts (enchmarks/benchmark_unlearning.py).
