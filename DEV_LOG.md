# DEV_LOG: VectorUnforget

## Metadati Autore & Privacy
- **Author:** Toskurim
- **Email:** toskurim@gmail.com
- **License:** AGPLv3
- **Repository:** https://github.com/Toskurim/vector-unforget

## Stato Attuale del Progetto (v3.1.0 Enterprise Industrial)
- **CI/CD Pipeline:** Attiva su GitHub Actions (Python 3.10, 3.11, 3.12).
- **Subspace Unlearning:** Accelerazione matriciale NumPy attiva (`project_matrix_orthogonal`).
- **Adapters Enterprise:** Pinecone, Weaviate, LanceDB, Qdrant, Pgvector, ChromaDB.
- **Middleware:** LangChain Retriever e LlamaIndex NodePostprocessor.
- **Adversarial Verification:** ReverseRAGVerifier con calcolo Zero Residual Leakage Score.
- **Packaging:** Conforme standard PEP 517/621 (`pyproject.toml`), build e validazione `twine` superate.
- **Test Suite:** 100% pass rate su pytest (15/15 test superati).

## Roadmap di Potenziamento Completata
- [x] **Fase 6: CI/CD Pipeline con GitHub Actions**
- [x] **Fase 7: NumPy Vectorized Subspace Engine**
- [x] **Fase 8: Nuovo Adapter Enterprise (LanceDB)**
- [x] **Fase 9: Packaging & Configurazione Distribuzione PyPI**

## Prossimi Passi Opzionali
- Rilascio di un tag Git `v3.1.0` su GitHub.
- Pubblicazione su PyPI tramite token API.