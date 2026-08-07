import json
from qdrant_client import QdrantClient
from qdrant_client.http import models

# Test 1: Verifica Import del Pacchetto installato
try:
    from vector_unforget import VectorUnforgetEngine, QdrantAdapter, PgvectorAdapter, ChromaAdapter
    print("✅ [TEST 1] Pacchetto vector-unforget e Adapter importati correttamente.")
except ImportError as e:
    print(f"❌ [TEST 1] Errore nell'importazione: {e}")
    exit(1)

# Inizializzazione DB in memoria
client = QdrantClient(":memory:")
collection_name = "test_suite_collection"

client.create_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(size=4, distance=models.Distance.COSINE)
)

# Popolamento dati di test (Mario Rossi + PII orfane)
client.upsert(
    collection_name=collection_name,
    points=[
        models.PointStruct(
            id=1, 
            vector=[0.1, 0.2, 0.3, 0.4], 
            payload={"text": "Contratto Mario Rossi. Email: m.rossi@company.com, CF: RSSMRA80A01H501U, Tel: +39 3331234567"}
        ),
        models.PointStruct(
            id=2, 
            vector=[0.2, 0.1, 0.4, 0.3], 
            payload={"text": "Log orfano legato solo al Codice Fiscale RSSMRA80A01H501U e alla mail m.rossi@company.com"}
        ),
        models.PointStruct(
            id=3, 
            vector=[0.9, 0.8, 0.7, 0.6], 
            payload={"text": "Nota sicura relativa all'utente Luigi Verdi."}
        ),
    ]
)

adapter = QdrantAdapter(client=client, collection_name=collection_name)
engine = VectorUnforgetEngine(adapter=adapter, db_name="qdrant_suite_test")

# Test 2: Simulazione (Dry Run)
dry_res = engine.purge_user("Mario Rossi", dry_run=True)
count_after_dry = client.count(collection_name=collection_name).count

if dry_res["status"] == "SIMULATION_SUCCESSFUL" and count_after_dry == 3:
    print("✅ [TEST 2] Dry Run completato: rilevati 2 vettori da eliminare, 0 vettori cancellati dal DB.")
else:
    print(f"❌ [TEST 2] Fallito: status={dry_res['status']}, punti rimasti={count_after_dry}")

# Test 3: Rilevamento PII Avanzate
extracted_pii = dry_res.get("secondary_pii_extracted", [])
has_cf = any("RSSMRA80A01H501U" in pii for pii in extracted_pii)
has_email = any("m.rossi@company.com" in pii for pii in extracted_pii)

if has_cf and has_email:
    print(f"✅ [TEST 3] Estrazione PII avanzata riuscita! Trovati CF ed Email: {extracted_pii}")
else:
    print(f"❌ [TEST 3] Fallito: PII estratte incomplete -> {extracted_pii}")

# Test 4: Purge Reale e Certificato Audit SHA-256
real_res = engine.purge_user("Mario Rossi", dry_run=False)
count_after_real = client.count(collection_name=collection_name).count

if real_res["status"] == "PURGED_SUCCESSFULLY" and count_after_real == 1 and "signature_sha256" in real_res:
    print(f"✅ [TEST 4] Purge reale eseguito: rimasto solo {count_after_real} vettore sicuro.")
    print(f"🔒 Audit Certificate SHA-256: {real_res['signature_sha256']}")
else:
    print(f"❌ [TEST 4] Fallito Purge Reale: punti rimasti={count_after_real}")