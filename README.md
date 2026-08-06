# VectorUnforget 🛡️ Vector DB Right-to-be-Forgotten Engine

VectorUnforget is a specialized python engine designed to enforce GDPR compliance (Right to be Forgotten) across Vector Databases used in RAG (Retrieval-Augmented Generation) architectures.

## 🚀 Key Features

- **Cascading PII Erasure:** Identifies primary entries, extracts secondary PII (emails, phone numbers), and purges orphaned entries lacking explicit name references.
- **Name Variant & Alias Engine:** Automatically generates and matches name permutations (e.g., `Mario Rossi`, `M. Rossi`, `Rossi M.`).
- **Cryptographic Audit Trail:** Generates a tamper-proof SHA-256 signed JSON certificate of erasure for compliance auditors and DPOs.

## 📦 Installation & Setup

1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/vector-unforget.git](https://github.com/YOUR_USERNAME/vector-unforget.git)
   cd vector-unforget