from typing import List, Dict, Any
import re
import spacy
from vector_unforget.adapters.base import BaseVectorAdapter
from auditor import AuditLogger
class VectorUnforgetEngine:
    def __init__(self, adapter: BaseVectorAdapter, db_name: str = "vector_db"):
        self.adapter = adapter
        self.db_name = db_name
        self.nlp = spacy.load("en_core_web_sm")
        self.auditor = AuditLogger()

    def generate_name_variants(self, name: str) -> List[str]:
        parts = name.strip().split()
        if len(parts) < 2:
            return [name]
        first, last = parts[0], parts[-1]
        return list(set([
            name,
            f"{first[0]}. {last}",
            f"{last} {first}",
            f"{last}, {first[0]}."
        ]))

    def purge_user(self, target_name: str) -> Dict[str, Any]:
        docs = self.adapter.fetch_all_documents()
        variants = self.generate_name_variants(target_name)
        
        ids_to_purge = []
        secondary_pii = set()

        # Phase 1: Identificazione diretta e estrazione PII secondarie (email, telefoni)
        for doc in docs:
            text = doc['text']
            matched = any(re.search(rf"\b{re.escape(v)}\b", text, re.IGNORECASE) for v in variants)
            
            if matched:
                ids_to_purge.append(doc['id'])
                # Estrazione pattern email e numeri di telefono
                emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
                phones = re.findall(r'\+?\d[\d -]{8,}\d', text)
                secondary_pii.update(emails)
                secondary_pii.update(phones)

        # Phase 2: Cascading Purge per vettori orfani contenenti PII secondarie
        if secondary_pii:
            for doc in docs:
                if doc['id'] in ids_to_purge:
                    continue
                text = doc['text']
                if any(pii in text for pii in secondary_pii):
                    ids_to_purge.append(doc['id'])

        # Esecuzione eliminazione tramite Adapter
        deleted_count = self.adapter.delete_documents_by_ids(ids_to_purge)

        # Generazione Certificato Audit SHA-256
        audit_certificate = self.auditor.log_purge(
            db_name=self.db_name,
            target_name=target_name,
            purged_ids=ids_to_purge,
            secondary_pii_found=list(secondary_pii)
        )

        return audit_certificate