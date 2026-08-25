# DEV_LOG: VectorUnforget

## Metadati Autore & Privacy
- **Author:** Toskurim
- **Email:** toskurim@gmail.com
- **License:** AGPLv3
- **Repository:** https://github.com/Toskurim/vector-unforget

## Stato Attuale del Progetto (v2.4.0)
- **Core Engine:** Cascading PII Erasure attivo con supporto regex & spaCy NER.
- **PII Coperte:** Globali (US SSN, UK NINO, CA SIN, IT CF, IPv4/IPv6, IBAN, Carte di Credito, Telefoni internazionali).
- **Audit & Safety:** Dry Run simulation attiva; certificati di bonifica SHA-256 JSON firmati.
- **Adapters Supportati:** Qdrant, Pgvector (PostgreSQL), ChromaDB.
- **Middleware Integrati:** 
  - `VectorUnforgetRetriever` per LangChain.
  - `VectorUnforgetNodePostprocessor` per LlamaIndex.
- **Verification Engine:** 
  - `ReverseRAGVerifier` con calcolo del *Zero Residual Leakage Score* e test avversari post-cancellazione.

## Roadmap di Sviluppo
- [x] **Fase 1: Framework Middleware (Completata)**
- [x] **Fase 2: Reverse RAG Verification Engine (Completata)**
- [ ] **Fase 3: Graph-Based Cascading Erasure (In Corso)**
  - Risoluzione entità a N-livelli con grafo di co-occorrenza dinamico.
- [ ] **Fase 4: Nuovi Adapters Enterprise**
  - Pinecone, Weaviate, Milvus.
- [ ] **Fase 5: Semantic Subspace Projection**
  - Proiezioni ortogonali nello spazio vettoriale.

## Prossima Azione Immediata
- Creare il modulo `vector_unforget/graph_resolver.py` per la risoluzione ad albero/grafo delle entità correlate.