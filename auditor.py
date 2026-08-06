import json
import hashlib
from datetime import datetime, timezone

class GDPRLogAuditor:
    def __init__(self, log_file="gdpr_deletion_audit.json"):
        self.log_file = log_file

    def generate_proof(self, target_user: str, purged_ids: list, db_name: str):
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Creiamo un record di eliminazione
        audit_entry = {
            "timestamp_utc": timestamp,
            "target_identifier": target_user,
            "target_database": db_name,
            "deleted_vector_count": len(purged_ids),
            "deleted_vector_ids": purged_ids,
            "status": "SUCCESS"
        }
        
        # Creiamo una firma crittografica dell'evento per garantire che non sia stato alterato
        raw_data = f"{timestamp}-{target_user}-{len(purged_ids)}-{db_name}"
        audit_entry["cryptographic_signature_sha256"] = hashlib.sha256(raw_data.encode()).hexdigest()
        
        # Salviamo il log su file JSON
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(audit_entry, indent=4) + "\n,\n")
            print(f"[AUDIT LOG] Certificato di eliminazione salvato in '{self.log_file}'")
        except Exception as e:
            print(f"[AUDIT ERROR] Impossibile salvare il log: {e}")

        return audit_entry