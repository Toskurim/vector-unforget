# DEV_LOG: VectorUnforget

## Metadati Autore & Privacy
- **Author:** Toskurim
- **Email:** toskurim@gmail.com
- **License:** AGPLv3
- **Repository:** https://github.com/Toskurim/vector-unforget

## Stato Attuale del Progetto (v3.1.0 Enterprise Industrial)
- **CI/CD Pipeline:** Completata (GitHub Actions multi-versione 3.10, 3.11, 3.12).
- **Subspace Unlearning:** Accelerazione matriciale batch attiva (`project_matrix_orthogonal`).
- **Adapters:** Qdrant, Pgvector, ChromaDB, Pinecone, Weaviate, LanceDB.
- **Middleware:** LangChain Retriever e LlamaIndex NodePostprocessor.
- **Verification:** ReverseRAGVerifier con calcolo Zero Residual Leakage Score.
- **Graph Engine:** PIIEntityGraph con decadimento confidenza multi-hop.

## Nuova Roadmap di Potenziamento
- [x] **Fase 6: CI/CD Pipeline con GitHub Actions**
- [x] **Fase 7: NumPy Vectorized Subspace Engine**
- [x] **Fase 8: Nuovo Adapter Enterprise (LanceDB)**
- [ ] **Fase 9: Packaging & Configurazione Distribuzione PyPI**

## Prossima Azione Immediata
- Eseguire i test con pytest (ora 15 test attesi) e inviare il commit.