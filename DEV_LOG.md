# DEV_LOG: VectorUnforget

## Metadati Autore & Privacy
- **Author:** Toskurim
- **Email:** toskurim@gmail.com
- **License:** AGPLv3
- **Repository:** https://github.com/Toskurim/vector-unforget

## Stato Attuale del Progetto (v3.0.0 Enterprise Ready)
- **Core Engine:** Cascading PII Erasure attivo con supporto regex & spaCy NER.
- **PII Coperte:** Globali (US SSN, UK NINO, CA SIN, IT CF, IPv4/IPv6, IBAN, Carte di Credito, Telefoni internazionali).
- **Audit & Safety:** Dry Run simulation; certificati di bonifica SHA-256 JSON firmati.
- **Adapters Supportati:** Qdrant, Pgvector (PostgreSQL), ChromaDB, Pinecone, Weaviate.
- **Middleware Integrati:** 
  - `VectorUnforgetRetriever` per LangChain.
  - `VectorUnforgetNodePostprocessor` per LlamaIndex.
- **Verification Engine:** 
  - `ReverseRAGVerifier` con calcolo del *Zero Residual Leakage Score* e test avversari post-cancellazione.
- **Graph Cascading Engine:** 
  - `PIIEntityGraph` con multi-hop traversing a decadimento di confidenza per bonifiche transitive.
- **Vector Space Unlearning:**
  - `SubspaceProjector` con proiezione ortogonale e annullamento semantico nello spazio vettoriale.

## Roadmap di Sviluppo
- [x] **Fase 1: Framework Middleware (Completata)**
- [x] **Fase 2: Reverse RAG Verification Engine (Completata)**
- [x] **Fase 3: Graph-Based Cascading Erasure (Completata)**
- [x] **Fase 4: Nuovi Adapters Enterprise (Completata)**
- [x] **Fase 5: Semantic Subspace Projection (Completata)**

## Note di Rilascio
- Architettura v3.0.0 pronta per packaging PyPI e pubblicazione open-source.