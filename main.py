import chromadb
from vector_unforget.engine import VectorUnforgetEngine

# Setup DB
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="production_rag_db")

# Inseriamo un documento "orfano" (ID doc_4) che contiene SOLO l'email ma NON il nome!
documents = [
    "Configurazione rete aziendale.",
    "L'utente Mario Rossi (mario.rossi@example.com) ha richiesto l'accesso.",
    "Log di sistema standard.",
    "Notifica inviata con successo a mario.rossi@example.com per conferma recupero password." # Nessun nome specificato qui!
]
ids = [f"doc_{i}" for i in range(len(documents))]
collection.add(documents=documents, ids=ids)

# Inizializziamo ed eseguiamo l'engine
engine = VectorUnforgetEngine(collection=collection, db_name="production_rag_db")
engine.purge_user("Mario Rossi")

# Verifica finale
print(f"\nDocumenti rimasti nel DB: {collection.count()}")
for doc in collection.get()['documents']:
    print(f" - {doc}")