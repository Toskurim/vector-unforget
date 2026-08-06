import chromadb
from presidio_analyzer import AnalyzerEngine

print("Inizializzazione in corso...")

# 1. Inizializziamo ChromaDB in memoria (locale) e l'analizzatore PII
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="gdpr_test_db")
analyzer = AnalyzerEngine()

# 2. Documenti di test (alcuni contengono dati personali di "Mario Rossi")
documents = [
    "Il server web gira sulla porta 8080 con configurazione NGINX.",
    "L'utente Mario Rossi (email: mario.rossi@example.com) ha richiesto l'aggiornamento dei permessi.",
    "Il bug relativo al rendering delle immagini è stato risolto nella release v2.1.",
    "Note interne: Contattare Mario Rossi al numero 333-1234567 per il rinnovo del contratto.",
    "La documentazione delle API REST è disponibile sul repository GitHub aziendale."
]
ids = [f"id_{i}" for i in range(len(documents))]

# Inseriamo i documenti nel Vector DB (generazione embedding automatica)
collection.add(documents=documents, ids=ids)
print(f"--- Inseriti {collection.count()} documenti nel Vector DB ---\n")

# 3. Funzione di scansione e bonifica GDPR
def scan_and_purge_user(user_name: str):
    print(f"Sto scansionando il DB per identificare dati di: '{user_name}'...")
    
    results = collection.get()
    all_docs = results['documents']
    all_ids = results['ids']
    
    ids_to_delete = []

    for doc_id, text in zip(all_ids, all_docs):
        # Analisi NLP per trovare il nome o entità correlate
        if user_name.lower() in text.lower():
            ids_to_delete.append(doc_id)
            print(f"[MATCH TROVATO] Trovata corrispondenza nell'ID '{doc_id}':\n    -> \"{text}\"")
    
    # Cancellazione dei vettori dal Vector DB
    if ids_to_delete:
        collection.delete(ids=ids_to_delete)
        print(f"\n[GDPR PURGE] Rimosso/i {len(ids_to_delete)} vettore/i dal database.")
    else:
        print("\nNessun dato personale trovato per l'utente specificato.")

# 4. Eseguiamo la bonifica per "Mario Rossi"
scan_and_purge_user("Mario Rossi")

# 5. Stato finale del DB
print(f"\n--- Documenti rimasti nel DB dopo la bonifica: {collection.count()} ---")
remaining = collection.get()
for doc in remaining['documents']:
    print(f" - {doc}")