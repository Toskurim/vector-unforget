VectorUnforget 🛡️ Vector DB Right-to-be-Forgotten Engine
VectorUnforget is a specialized Python engine designed to enforce GDPR compliance (Right to be Forgotten) across Vector Databases used in RAG (Retrieval-Augmented Generation) architectures.

🚀 Key Features
Cascading PII Erasure: Identifies primary entries, extracts secondary PII (emails, phone numbers), and purges orphaned entries lacking explicit name references.

Name Variant & Alias Engine: Automatically generates and matches name permutations (e.g., Mario Rossi, M. Rossi, Rossi M.).

Cryptographic Audit Trail: Generates a tamper-proof SHA-256 signed JSON certificate of erasure for compliance auditors and DPOs.

📦 Installation & Setup
Clone the repository:

Bash
git clone https://github.com/Toskurim/vector-unforget.git
cd vector-unforget
Set up virtual environment & dependencies:

Bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m spacy download en_core_web_sm
🛠️ Usage Example
Python
import chromadb
from vector_unforget.engine import VectorUnforgetEngine

# 1. Initialize Vector DB
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="production_rag_db")

# 2. Initialize Engine
engine = VectorUnforgetEngine(collection=collection, db_name="production_rag_db")

# 3. Execute Cascading Purge
audit_log = engine.purge_user("Mario Rossi")
📄 License
This project is licensed under the GNU Affero General Public License v3.0 (AGPLv3) - see the LICENSE file for details. Commercial licensing options are available for enterprise integration.