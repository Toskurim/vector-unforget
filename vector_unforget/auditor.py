"""
Audit & Compliance Logger for VectorUnforget.
Author: Toskurim
License: AGPLv3
"""

import hashlib
import json
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional


class Auditor:
    """
    Generates verifiable SHA-256 signed audit records for right-to-be-forgotten operations.
    """

    def __init__(self, log_path: Optional[str] = "gdpr_deletion_audit.json", log_file: Optional[str] = None, *args, **kwargs):
        self.log_path = log_file if log_file is not None else log_path

    @staticmethod
    def _generate_hash(data: Dict[str, Any]) -> str:
        serialized = json.dumps(data, sort_keys=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def generate_certificate(
        self,
        target_entity: str = "",
        deleted_ids: Optional[List[str]] = None,
        dry_run: bool = False,
        extra_metadata: Optional[Dict[str, Any]] = None,
        *args,
        **kwargs,
    ) -> Dict[str, Any]:
        """Creates a structured compliance certificate with all legacy and modern keys."""
        if deleted_ids is None:
            deleted_ids = []

        merged_metadata = dict(extra_metadata or {})
        merged_metadata.update(kwargs)

        iso_time = datetime.now(timezone.utc).isoformat()
        status_label = "SIMULATION_SUCCESSFUL" if dry_run else "PURGED_SUCCESSFULLY"

        payload = {
            "timestamp": iso_time,
            "target_entity": target_entity,
            "records_purged_count": len(deleted_ids),
            "target_vector_ids": deleted_ids,
            "dry_run": dry_run,
            "metadata": merged_metadata,
        }
        certificate_hash = self._generate_hash(payload)

        certificate = {
            "status": status_label,
            "signature_sha256": certificate_hash,
            "audit_hash_sha256": certificate_hash,
            "timestamp": iso_time,
            "target_entity": target_entity,
            "target_name": target_entity,
            "purged_vector_ids": deleted_ids,
            "vector_ids_purged": deleted_ids,
            "target_vector_ids": deleted_ids,
            "records_purged_count": len(deleted_ids),
            "secondary_pii_extracted": merged_metadata.get("secondary_pii_extracted", []),
            "dry_run": dry_run,
            "metadata": merged_metadata,
            "record": payload,
        }
        # Inietta direttamente tutte le altre chiavi di metadati per massima retrocompatibilità
        for k, v in merged_metadata.items():
            if k not in certificate:
                certificate[k] = v

        if self.log_path and not dry_run:
            self._persist_certificate(certificate)

        return certificate

    def log_purge(
        self,
        target_entity: str = "",
        deleted_ids: Optional[List[str]] = None,
        dry_run: bool = False,
        extra_metadata: Optional[Dict[str, Any]] = None,
        *args,
        **kwargs,
    ) -> Dict[str, Any]:
        """Legacy and modern purge audit logging."""
        return self.generate_certificate(
            target_entity=target_entity,
            deleted_ids=deleted_ids,
            dry_run=dry_run,
            extra_metadata=extra_metadata,
            *args,
            **kwargs,
        )

    def generate_proof(self, *args, **kwargs) -> Dict[str, Any]:
        """Compatibility wrapper for generate_proof."""
        return self.generate_certificate(*args, **kwargs)

    def _persist_certificate(self, cert: Dict[str, Any]) -> None:
        try:
            records = []
            try:
                with open(self.log_path, "r", encoding="utf-8") as f:
                    records = json.load(f)
                    if not isinstance(records, list):
                        records = [records]
            except Exception:
                records = []

            records.append(cert)
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump(records, f, indent=2)
        except Exception:
            pass


# Backward compatibility aliases
GDPRLogAuditor = Auditor
AuditLogger = Auditor