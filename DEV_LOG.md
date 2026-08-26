# DEV_LOG: VectorUnforget

## Metadati Autore & Privacy
- **Author:** Toskurim
- **Email:** toskurim@gmail.com
- **License:** AGPLv3
- **Repository:** https://github.com/Toskurim/vector-unforget

## Stato Attuale del Progetto (v3.0.0 Enterprise Ready)
- **Core Engine:** Cascading PII Erasure attivo con regex & spaCy NER.
- **Adapters:** Qdrant, Pgvector, ChromaDB, Pinecone, Weaviate.
- **Middleware:** LangChain Retriever e LlamaIndex NodePostprocessor.
- **Verification:** ReverseRAGVerifier con calcolo Zero Residual Leakage Score.
- **Graph Engine:** PIIEntityGraph con decadimento confidenza multi-hop.
- **Subspace Unlearning:** SubspaceProjector per proiezione ortogonale.
- **Test Suite:** 100% pass rate su pytest (13/13 test passati).

## Nuova Roadmap di Potenziamento (v3.1.0 Enterprise Industrial)
- [ ] **Fase 6: CI/CD Pipeline con GitHub Actions (In Corso)**
  - Esecuzione automatica test su Python 3.10, 3.11, 3.12 a ogni push/PR.
- [ ] **Fase 7: NumPy Vectorized Subspace Engine**
  - Accelerazione algebrica matriciale ad alto throughput per dataset massivi.
- [ ] **Fase 8: Nuovo Adapter Enterprise (LanceDB / Milvus)**
  - Supporto nativo per database vettoriali serverless/on-premise ad alte prestazioni.
- [ ] **Fase 9: Packaging & Configurazione Distribuzione PyPI**
  - Predisposizione build wheel e tarball per `pip install vector-unforget`.

## Prossima Azione Immediata
- Creare la configurazione workflow `.github/workflows/ci.yml`.