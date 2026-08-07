# VectorUnforget 🛡️ Vector DB Right-to-be-Forgotten Engine

VectorUnforget is an enterprise-grade Python engine designed to enforce GDPR/CCPA compliance (Right to be Forgotten) across Vector Databases used in RAG (Retrieval-Augmented Generation) architectures.

## 🚀 Key Features

- **Multi-Vector DB Support (Adapter Pattern):** Out-of-the-box integration with **ChromaDB**, **Qdrant**, and **Pgvector (PostgreSQL)**, with an extensible architecture for enterprise vector stores.
- **Global PII Recognition (NER & Regex):** Identifies primary entries and automatically extracts secondary PII globally:
  - **Universal:** Emails, International Phone Numbers, Credit Cards, IBANs, IPv4/IPv6 Addresses.
  - **National Identifiers:** US SSN, UK NINO, Italian Fiscal Code, Canadian SIN, German Steuer-ID.
  - **Multilingual NER:** Powered by spaCy for custom entities (PERSON, ORG, GPE, FAC).
- **Dry Run Mode (Simulation):** Preview vectors and secondary PII targeted for removal before committing destructive deletes to production databases.
- **Cascading PII Erasure:** Automatically purges orphaned vector entries that share secondary PII even if the target name is not explicitly mentioned.
- **Name Variant Engine:** Automatically generates and matches name permutations (e.g., `Mario Rossi`, `M. Rossi`, `Rossi M.`).
- **Tamper-Proof Audit Trail:** Generates a SHA-256 signed JSON certificate of erasure for compliance auditors and DPOs.

## 📦 Installation & Setup

1. Install via pip (with optional extra dependencies):
   ```bash
   # Install core package
   pip install vector-unforget

   # Install with specific adapters (e.g., Qdrant or Pgvector)
   pip install "vector-unforget[qdrant]"
   pip install "vector-unforget[pgvector]"

   # Or install all adapters:
   pip install "vector-unforget[all]"
   ```

2. Download spaCy model for NER support:
   ```bash
   python -m spacy download en_core_web_sm
   ```

## 🛠️ Usage Examples

### 1. Global Dry Run (Simulation Mode)

```python
from qdrant_client import QdrantClient
from vector_unforget import VectorUnforgetEngine, QdrantAdapter

client = QdrantClient("http://localhost:6333")
adapter = QdrantAdapter(client=client, collection_name="production_rag")
engine = VectorUnforgetEngine(adapter=adapter, db_name="qdrant_prod")

# Run simulation detecting US SSN, IPv4, Emails, and phones globally
preview = engine.purge_user("John Smith", dry_run=True)
print("Vectors to be purged:", preview["vector_ids_to_be_purged"])
print("Secondary PII extracted:", preview["secondary_pii_extracted"])
```

### 2. Pgvector (PostgreSQL) Integration

```python
from vector_unforget import VectorUnforgetEngine, PgvectorAdapter

adapter = PgvectorAdapter(
    connection_string="postgresql://user:password@localhost:5432/rag_db",
    table_name="embeddings",
    id_column="id",
    text_column="content"
)

engine = VectorUnforgetEngine(adapter=adapter, db_name="pgvector_prod")

# Execute real cascading purge
audit_log = engine.purge_user("John Smith", dry_run=False)
```

## 📄 License

This project is licensed under the GNU Affero General Public License v3.0 (AGPLv3) - see the [LICENSE](LICENSE) file for details. Commercial licensing options are available for enterprise integration.