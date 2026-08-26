# VectorUnforget

[![CI Matrix](https://github.com/Toskurim/vector-unforget/actions/workflows/ci.yml/badge.svg)](https://github.com/Toskurim/vector-unforget/actions)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-brightgreen)](https://www.python.org/)

VectorUnforget is an enterprise-grade vector unlearning and cascading PII erasure framework designed for compliance with GDPR (Right to be Forgotten) and CCPA. It eliminates direct identifiers, resolves multi-hop identity graphs, and projects vector embeddings onto orthogonal subspaces to prevent knowledge leakage in RAG pipelines without requiring index retraining.

---

## Key Features

- Cascading PII Detection: Hybrid entity detection combining high-performance regular expressions and spaCy Named Entity Recognition (NER).
- Transient PII Graph Resolver: Maps multi-hop entity relationships with weighted confidence decay across conversational sessions.
- NumPy Accelerated Subspace Projection: High-throughput batch matrix projections eliminating target concept directions directly from vector representations.
- Multi-Engine Vector Adapters: Native support for Pinecone, Weaviate, LanceDB, Qdrant, Pgvector (PostgreSQL), and ChromaDB.
- RAG Middleware: Drop-in integrations for LangChain (VectorUnforgetRetriever) and LlamaIndex (VectorUnforgetNodePostprocessor).
- Adversarial Reverse RAG Verification: Post-deletion penetration probing providing automated Zero Residual Leakage Score audits.
- Enterprise Packaging: Fully PEP 517/621 compliant, tested across Python 3.10, 3.11, and 3.12 matrices.

---

## Architecture Overview

[ Ingestion / Query ]
        │
        ▼
[ PII Entity Graph Resolver ] ---> (Regex + spaCy NER Multi-hop)
        │
        ├──> [ Hard Erasure ] ------> Vector DB Adapters (Pinecone, LanceDB, Qdrant, etc.)
        │
        ├──> [ Subspace Projector ] -> High-Throughput Matrix Projection (NumPy)
        │
        ▼
[ Reverse RAG Adversarial Verifier ] ---> Zero Residual Leakage Audit Log

---

## Installation

### Basic Installation
pip install vector-unforget

### With Optional Adapter Dependencies
# Install with all vector databases and framework middleware
pip install "vector-unforget[all]"

# Install testing dependencies
pip install "vector-unforget[test]"

---

## Quickstart

### 1. Vector Subspace Unlearning (Batch Projection)
import numpy as np
from vector_unforget import SubspaceProjector

projector = SubspaceProjector()

# Embedding batch: 3 vectors of dimension 3
embeddings = np.array([
    [0.8, 0.6, 0.0],
    [0.6, 0.8, 0.0],
    [0.0, 1.0, 0.0]
], dtype=np.float32)

# Sensitive concept direction to eliminate
concept_vector = np.array([1.0, 0.0, 0.0], dtype=np.float32)

# Project orthogonal complement
unlearned_matrix = projector.project_matrix_orthogonal(embeddings, concept_vector, normalize=True)

### 2. Multi-Hop Graph Resolution
from vector_unforget import PIIEntityGraph

graph = PIIEntityGraph(decay_factor=0.85)
graph.add_relation("John Doe", "john.doe@company.com", relation_type="EMAIL")
graph.add_relation("john.doe@company.com", "IP_192.168.1.50", relation_type="NETWORK_LOG")

# Resolve all transient linked identities
erasure_targets = graph.resolve_associated_pii("John Doe", max_hops=2)

### 3. LanceDB Serverless Adapter
import lancedb
from vector_unforget.adapters import LanceDBAdapter

db = lancedb.connect("./data/lancedb")
table = db.open_table("documents")

adapter = LanceDBAdapter(table=table)
res = adapter.delete_documents_by_ids(["doc_101", "doc_102"], dry_run=False)
print(f"Deleted records: {res['deleted_count']}")

---

## Running the Test Suite

python -m pytest

---

## License & Author

- Author: Toskurim (toskurim@gmail.com)
- License: AGPL-3.0-or-later
- Repository: https://github.com/Toskurim/vector-unforget