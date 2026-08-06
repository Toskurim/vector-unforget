import chromadb
from presidio_analyzer import AnalyzerEngine, RecognizerResult

print("Avvio motore avanzato...")
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="gdpr_advanced_db")
analyzer = AnalyzerEngine()

# Dataset di test più complesso
documents = [
    "Configurazione server NGINX sulla porta 8080.",
    "L'utente Mario Rossi (mario.rossi@example.com) richiede l'aggiornamento dei permessi.",
    "Corretto il bug di rendering sulla release v2.1.",
    "Contattare Rossi M. al numero 333-1234567 per il rinnovo contrattuale.",
    "Nota di servizio: M. Rossi ha completato il passaggio di consegne.",
    "Documentazione API REST disponibile sul repository."
]
ids = [f"doc_{i}" for i in range(len(documents))]
collection.add(documents=documents, ids=ids)

def semantic_pii_purge(target_query: str, similarity_threshold: float = 0.5):
    print(f"\n--- Avvio bonifica avanzata per: '{target_query}' ---")
    
    # 1. Ricerca semantica nel Vector DB per identificare i chunk rilevanti
    results = collection.query(
        query_texts=[target_query],
        n_results=len(documents)
    )
    
    found_ids = results['ids'][0]
    found_docs = results['documents'][0]
    distances = results['distances'][0]
    
    ids_to_purge = []
    
    for doc_id, text, dist in zip(found_ids, found_docs, distances):
        # Minore è la distanza, maggiore è la somiglianza semantica
        # Analizziamo il testo con Microsoft Presidio per rilevare PII
        pii_results = analyzer.analyze(text=text, language="en")
        
        # Se c'è prossimità semantica o Presidio rileva dati personali pertinenti
        is_relevant = dist < 1.2  # Soglia di rilevanza vettoriale
        has_pii = len(pii_results) > 0
        
        if is_relevant and (target_query.lower() in text.lower() or has_pii):
            ids_to_purge.append(doc_id)
            detected_types = [p.entity_type for p in pii_results]
            print(f"[MATCH VETTORIALE] ID: {doc_id} | Distanza: {dist:.3f}")
            print(f"    Testo: \"{text}\"")
            print(f"    PII Rilevate: {detected_types if detected_types else 'Nessuna specifica'}\n")

    # 2. Cancellazione selettiva dal Vector DB
    if ids_to_purge:
        collection.delete(ids=ids_to_purge)
        print(f"[GDPR PURGE] Eliminati {len(ids_to_purge)} vettori dal database.")
    else:
        print("Nessun dato corrispondente trovato.")

# Eseguiamo la ricerca su una variante del nome
semantic_pii_purge("Mario Rossi")

# Check finale
print(f"\nDocumenti rimasti nel DB: {collection.count()}")
for doc in collection.get()['documents']:
    print(f" - {doc}")