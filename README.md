# VectorUnforget 🛡️ Vector DB Right-to-be-Forgotten Engine

VectorUnforget is a specialized Python engine designed to enforce GDPR compliance (Right to be Forgotten) across Vector Databases used in RAG (Retrieval-Augmented Generation) architectures.

## 🚀 Key Features

- **Multi-Vector DB Support (Adapter Pattern):** Out-of-the-box integration with **ChromaDB** and **Qdrant**, with an extensible architecture for adding enterprise vector stores (Pinecone, Pgvector, Weaviate).
- **Cascading PII Erasure:** Identifies primary entries, extracts secondary PII (emails, phone numbers), and purges orphaned entries lacking explicit name references.
- **Name Variant & Alias Engine:** Automatically generates and matches name permutations (e.g., `Mario Rossi`, `M. Rossi`, `Rossi M.`).
- **Cryptographic Audit Trail:** Generates a tamper-proof SHA-256 signed JSON certificate of erasure for compliance auditors and DPOs.

## 📦 Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Toskurim/vector-unforget.git
   cd vector-unforget
   ```

2. Set up virtual environment & dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

## 🛠️ Usage Examples

### 1. ChromaDB Integration

```python
import chromadb
from vector_unforget import VectorUnforgetEngine, ChromaAdapter

# Initialize Vector DB & Collection
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="production_rag_db")

# Initialize Adapter & Engine
adapter = ChromaAdapter(collection=collection)
engine = VectorUnforgetEngine(adapter=adapter, db_name="chroma_production")

# Execute Cascading Purge
audit_log = engine.purge_user("Mario Rossi")
```

### 2. Qdrant Integration

```python
from qdrant_client import QdrantClient
from vector_unforget import VectorUnforgetEngine, QdrantAdapter

# Initialize Qdrant Client
client = QdrantClient(url="http://localhost:6333")

# Initialize Adapter & Engine
adapter = QdrantAdapter(client=client, collection_name="production_rag_db")
engine = VectorUnforgetEngine(adapter=adapter, db_name="qdrant_production")

# Execute Cascading Purge
audit_log = engine.purge_user("Mario Rossi")
```

## 📄 License

This project is licensed under the GNU Affero General Public License v3.0 (AGPLv3) - see the [LICENSE](LICENSE) file for details. Commercial licensing options are available for enterprise integration.