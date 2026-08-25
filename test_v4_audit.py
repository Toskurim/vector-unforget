import chromadb
import re
from vector_unforget.auditor import GDPRLogAuditor

print("Avvio VectorUnforget Engine v4 (con GDPR Audit)...")

# 1. Inizializzazione DB e Auditor
chroma_client = chromadb.Client()
db_name = "gdpr_v4_db"
collection = chroma_client.create_collection(name=db_name)
auditor = GDPRLogAuditor(log_file="gdpr_deletion_audit.json")

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
    parts = full_name.split()
    aliases = [full_name]
    if len(parts) >= 2:
        first, last = parts[0], parts[-1]
        aliases.append(f"{first[0]}. {last}")
        aliases.append(f"{last} {first[0]}.")
        aliases.append(last)
    return aliases

def robust_purge_with_audit(user_name: str):
    print(f"\n--- Inizio procedura di purge avanzata per: '{user_name}' ---")
    
    aliases = generate_aliases(user_name)
    ids_to_purge = set()
    
    results = collection.get()
    all_docs = results['documents']
    all_ids = results['ids']
    
    for doc_id, text in zip(all_ids, all_docs):
        for alias in aliases:
            pattern = re.compile(r'\b' + re.escape(alias) + r'\b', re.IGNORECASE)
            if pattern.search(text):
                ids_to_purge.add(doc_id)
                print(f"[MATCH STRUTTURATO] Trovata variante '{alias}' in [{doc_id}]: \"{text}\"")
                break

    # Cancellazione e Audit
    if ids_to_purge:
        purge_list = sorted(list(ids_to_purge))
        collection.delete(ids=purge_list)
        print(f"\n[GDPR PURGE] Rimosso/i {len(purge_list)} vettore/i dal database.")
        
        # Generazione automatica del report GDPR
        auditor.generate_proof(target_user=user_name, purged_ids=purge_list, db_name=db_name)
    else:
        print("\nNessun dato trovato.")

# Eseguiamo la bonifica
robust_purge_with_audit("Mario Rossi")