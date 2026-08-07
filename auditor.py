import json
import hashlib
from datetime import datetime
from typing import List, Dict, Any

class AuditLogger:
    def __init__(self, log_filename: str = "gdpr_deletion_audit.json"):
        self.log_filename = log_filename

    def log_purge(self, db_name: str, target_name: str, purged_ids: List[str], secondary_pii_found: List[str]) -> Dict[str, Any]:
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        payload = {
            "timestamp": timestamp,
            "db_name": db_name,
            "target_name": target_name,
            "purged_vector_ids": purged_ids,
            "secondary_pii_extracted": secondary_pii_found,
            "status": "PURGED_SUCCESSFULLY"
        }
        
        # Generazione firma crittografica SHA-256 del payload
        raw_data = json.dumps(payload, sort_keys=True)
        signature = hashlib.sha256(raw_data.encode("utf-8")).hexdigest()
        
        payload["signature_sha256"] = signature
        
        # Salva a file il registro di audit
        try:
            with open(self.log_filename, "a", encoding="utf-8") as f:
                f.write(json.dumps(payload) + "\n")
        except Exception as e:
            print(f"Errore durante la scrittura dell'audit log: {e}")
            
        return payload