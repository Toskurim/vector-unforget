from qdrant_client import QdrantClient
from qdrant_client.http import models
from vector_unforget import VectorUnforgetEngine, QdrantAdapter

# 1. Inizializza Qdrant in memoria (in-memory per il test)
client = QdrantClient(":memory:")
collection_name = "test_rag_qdrant"

client.create_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(size=4, distance=models.Distance.COSINE)
)

# 2. Inserisci vettori di prova con PII primarie e secondarie
client.upsert(
    collection_name=collection_name,
    points=[
        models.PointStruct(id=1, vector=[0.1, 0.2, 0.3, 0.4], payload={"text": "User Mario Rossi profile. Email: mario.rossi@example.com"}),
        models.PointStruct(id=2, vector=[0.2, 0.1, 0.4, 0.3], payload={"text": "Log entry without name, but secondary PII: mario.rossi@example.com"}),
        models.PointStruct(id=3, vector=[0.9, 0.8, 0.7, 0.6], payload={"text": "Safe note regarding another employee Luigi Verdi"}),
    ]
)

# 3. Collega l'Adapter Qdrant ed esegui VectorUnforgetEngine
adapter = QdrantAdapter(client=client, collection_name=collection_name)
engine = VectorUnforgetEngine(adapter=adapter, db_name="qdrant_memory")

print("--- ESECUZIONE PURGE SU QDRANT ---")
certificate = engine.purge_user("Mario Rossi")

print(f"Status: {certificate['status']}")
print(f"Vettori eliminati (IDs): {certificate['purged_vector_ids']}")
print(f"PII secondaria trovata: {certificate['secondary_pii_extracted']}")
print(f"SHA-256 Signature: {certificate['signature_sha256']}")