from qdrant_client import QdrantClient
from qdrant_client.http import models
from vector_unforget import VectorUnforgetEngine, QdrantAdapter

client = QdrantClient(":memory:")
collection_name = "test_pii_collection"

client.create_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(size=4, distance=models.Distance.COSINE)
)

client.upsert(
    collection_name=collection_name,
    points=[
        models.PointStruct(id=1, vector=[0.1, 0.2, 0.3, 0.4], payload={"text": "Contratto Mario Rossi. Codice Fiscale: RSSMRA80A01H501U"}),
        models.PointStruct(id=2, vector=[0.2, 0.1, 0.4, 0.3], payload={"text": "Transazione finanziaria legata a Codice Fiscale RSSMRA80A01H501U"}),
    ]
)

adapter = QdrantAdapter(client=client, collection_name=collection_name)
engine = VectorUnforgetEngine(adapter=adapter, db_name="qdrant_pii_test")

result = engine.purge_user("Mario Rossi", dry_run=True)

print("--- RISULTATO ESTRAZIONE PII AVANZATA ---")
print(f"PII Estratte: {result['secondary_pii_extracted']}")
print(f"Vettori individuati: {result['vector_ids_to_be_purged']}")