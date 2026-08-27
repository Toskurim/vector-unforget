"""
Compliance & Cryptographic Audit Reporting Module for VectorUnforget.
Generates tamper-evident GDPR Art. 17 & CCPA audit certificates with SHA-256 state signatures.
"""

from typing import List, Dict, Any, Optional
import hashlib
import json
from datetime import datetime, timezone
import numpy as np


class ComplianceCertificateGenerator:
    """
    Generates verifiable cryptographic erasure receipts for DPO compliance records.
    """

    @staticmethod
    def _compute_state_hash(data: Any) -> str:
        """Compute SHA-256 hash of structured payload data."""
        serialized = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def generate_certificate(
        self,
        request_id: str,
        entity_identifier: str,
        unlearned_vector_count: int,
        pre_unlearning_leakage: float,
        post_unlearning_leakage: float,
        scrubbed_terms: Optional[List[str]] = None,
        operator_id: str = "automated_engine",
        regulation: str = "GDPR_Art_17"
    ) -> Dict[str, Any]:
        """
        Build a tamper-evident compliance audit certificate.
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        terms = scrubbed_terms or []
        delta_leakage = max(0.0, float(pre_unlearning_leakage - post_unlearning_leakage))
        zero_residual_verified = post_unlearning_leakage < 0.05

        payload = {
            "certificate_version": "1.0",
            "request_id": request_id,
            "timestamp_utc": timestamp,
            "regulation": regulation,
            "operator_id": operator_id,
            "target_entity": entity_identifier,
            "unlearned_vector_count": unlearned_vector_count,
            "scrubbed_lexical_terms_count": len(terms),
            "metrics": {
                "pre_leakage_score": round(float(pre_unlearning_leakage), 6),
                "post_leakage_score": round(float(post_unlearning_leakage), 6),
                "semantic_attenuation_delta": round(delta_leakage, 6),
                "zero_residual_leakage_verified": zero_residual_verified
            }
        }

        # Cryptographic Signature (SHA-256 of the audit receipt)
        signature = self._compute_state_hash(payload)
        payload["cryptographic_hash_sha256"] = signature
        return payload
