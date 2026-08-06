import chromadb
from presidio_analyzer import AnalyzerEngine
import re

print("Avvio VectorUnforget Engine v3...")
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="gdpr_v3_db")
analyzer = AnalyzerEngine()

# Dataset di test
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

def generate_aliases(full_name: str):
    """Genera varianti del nome (es. Mario Rossi -> M. Rossi, Rossi M.)"""
    parts = full_name.split()
    aliases = [full_name]
    if len(parts) >= 2:
        first, last = parts[0], parts[-1]
        aliases.append(f"{first[0]}. {last}") # M. Rossi
        aliases.append(f"{last} {first[0]}.") # Rossi M.
        aliases.append(last)                 # Rossi
    return aliases

def robust_purge(user_name: str):
    print(f"\n--- Inizio procedura di purge avanzata per: '{user_name}' ---")
    
    aliases = generate_aliases(user_name)
    print(f"Varianti nome generate per la ricerca: {aliases}")
    
    ids_to_purge = set()
    
    # 1. Scansione testuale diretta su tutte le varianti
    results = collection.get()
    all_docs = results['documents']
    all_ids = results['ids']
    
    for doc_id, text in zip(all_ids, all_docs):
        # Controlla se una qualsiasi variante è presente nel testo
        for alias in aliases:
            # Match case-insensitive con confini di parola
            pattern = re.compile(r'\b' + re.escape(alias) + r'\b', re.IGNORECASE)
            if pattern.search(text):
                ids_to_purge.add(doc_id)
                print(f"[MATCH STRUTTURATO] Trovata variante '{alias}' in [{doc_id}]: \"{text}\"")
                break

    # 2. Cancellazione fisica
    if ids_to_purge:
        purge_list = list(ids_to_purge)
        collection.delete(ids=purge_list)
        print(f"\n[GDPR PURGE] Rimosso/i {len(purge_list)} vettore/i dal database.")
    else:
        print("\nNessun dato trovato.")

# Eseguiamo il test
robust_purge("Mario Rossi")

# Verifica finale
print(f"\nDocumenti rimasti nel DB: {collection.count()}")
for doc in collection.get()['documents']:
    print(f" - {doc}")