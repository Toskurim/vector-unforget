from qdrant_client import QdrantClient
from qdrant_client.http import models
from vector_unforget import VectorUnforgetEngine, QdrantAdapter

# Inizializza Qdrant in memoria
client = QdrantClient(":memory:")
collection_name = "test_dry_run_collection"

client.create_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(size=4, distance=models.Distance.COSINE)
)

# Inserimento dati di test
client.upsert(
    collection_name=collection_name,
    points=[
        models.PointStruct(id=101, vector=[0.1, 0.2, 0.3, 0.4], payload={"text": "User Mario Rossi. Email: m.rossi@company.com"}),
        models.PointStruct(id=102, vector=[0.2, 0.1, 0.4, 0.3], payload={"text": "Log note with email m.rossi@company.com"}),
    ]
)

adapter = QdrantAdapter(client=client, collection_name=collection_name)
engine = VectorUnforgetEngine(adapter=adapter, db_name="qdrant_test")

print("--- 1. TEST DRY RUN (SIMULAZIONE) ---")
simulation_result = engine.purge_user("Mario Rossi", dry_run=True)
print(simulation_result)

# Verifica che i punti siano ancora nel DB
points_count = client.count(collection_name=collection_name).count
print(f"Punti ancora presenti nel DB dopo Dry Run: {points_count}")

print("\n--- 2. TEST ESECUZIONE REALE ---")
real_result = engine.purge_user("Mario Rossi", dry_run=False)
print(f"Status reale: {real_result['status']}")

points_count_after = client.count(collection_name=collection_name).count
print(f"Punti presenti nel DB dopo Purge Reale: {points_count_after}")