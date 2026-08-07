from qdrant_client import QdrantClient
from qdrant_client.http import models
from vector_unforget import VectorUnforgetEngine, QdrantAdapter

client = QdrantClient(":memory:")
collection_name = "test_global_collection"

client.create_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(size=4, distance=models.Distance.COSINE)
)

# Dati di test internazionali
client.upsert(
    collection_name=collection_name,
    points=[
        models.PointStruct(
            id=1, 
            vector=[0.1, 0.2, 0.3, 0.4], 
            payload={"text": "User John Smith. US SSN: 123-45-6789, IP: 192.168.1.50, Email: john.smith@global.com"}
        ),
        models.PointStruct(
            id=2, 
            vector=[0.2, 0.1, 0.4, 0.3], 
            payload={"text": "Log entry linked to US SSN 123-45-6789 without explicit name."}
        ),
        models.PointStruct(
            id=3, 
            vector=[0.9, 0.8, 0.7, 0.6], 
            payload={"text": "Unrelated vector for Jane Doe."}
        ),
    ]
)

adapter = QdrantAdapter(client=client, collection_name=collection_name)
engine = VectorUnforgetEngine(adapter=adapter, db_name="qdrant_global_test")

result = engine.purge_user("John Smith", dry_run=True)

print("--- TEST PII GLOBALI (USA / INTERNAZIONALE) ---")
print(f"PII Estratte: {result['secondary_pii_extracted']}")
print(f"Vettori individuati: {result['vector_ids_to_be_purged']}")

assert "123-45-6789" in result['secondary_pii_extracted'], "SSN Americano non trovato!"
assert "john.smith@global.com" in result['secondary_pii_extracted'], "Email non trovata!"
assert len(result['vector_ids_to_be_purged']) == 2, "Cascading Purge fallito sui vettori orfani!"

print("\n✅ TUTTI I TEST GLOBALI SUPERATI CON SUCCESSO!")