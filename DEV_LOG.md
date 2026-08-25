# DEV_LOG: VectorUnforget

## Metadati Autore & Privacy
- **Author:** Toskurim
- **Email:** toskurim@gmail.com
- **License:** AGPLv3
- **Repository:** https://github.com/Toskurim/vector-unforget

## Stato Attuale del Progetto (v2.7.0)
- **Core Engine:** Cascading PII Erasure attivo con supporto regex & spaCy NER.
- **PII Coperte:** Globali (US SSN, UK NINO, CA SIN, IT CF, IPv4/IPv6, IBAN, Carte di Credito, Telefoni internazionali).
- **Audit & Safety:** Dry Run simulation attiva; certificati di bonifica SHA-256 JSON firmati.
- **Adapters Supportati:** Qdrant, Pgvector (PostgreSQL), ChromaDB, Pinecone, Weaviate.
- **Middleware Integrati:** 
  - `VectorUnforgetRetriever` per LangChain.
  - `VectorUnforgetNodePostprocessor` per LlamaIndex.
- **Verification Engine:** 
  - `ReverseRAGVerifier` con calcolo del *Zero Residual Leakage Score* e test avversari post-cancellazione.
- **Graph Cascading Engine:** 
  - `PIIEntityGraph` con multi-hop traversing a decadimento di confidenza per bonifiche transitive.

## Roadmap di Sviluppo
- [x] **Fase 1: Framework Middleware (Completata)**
- [x] **Fase 2: Reverse RAG Verification Engine (Completata)**
- [x] **Fase 3: Graph-Based Cascading Erasure (Completata)**
- [x] **Fase 4: Nuovi Adapters Enterprise (Completata)**
  - Pinecone & Weaviate operativi e integrati.
- [ ] **Fase 5: Semantic Subspace Projection (In Corso)**
  - Proiezioni ortogonali nello spazio vettoriale per unlearning semantico puro.

## Prossima Azione Immediata
- Creare il modulo `vector_unforget/subspace_projection.py` (Fase 5: Unlearning Vettoriale).