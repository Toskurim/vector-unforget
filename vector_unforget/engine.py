from typing import List, Dict, Any
import re
import spacy
from vector_unforget.adapters.base import BaseVectorAdapter
from vector_unforget.auditor import AuditLogger

class VectorUnforgetEngine:
    def __init__(self, adapter: BaseVectorAdapter, db_name: str = "vector_db"):
        self.adapter = adapter
        self.db_name = db_name
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except Exception:
            self.nlp = None
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

    def extract_pii_from_text(self, text: str) -> List[str]:
        pii = set()
        
        # Email
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
        pii.update(emails)

        # Telefoni
        phones = re.findall(r'\+?\d[\d -]{8,}\d', text)
        pii.update(phones)

        # Codice Fiscale Italiano
        cf_matches = re.findall(r'\b[A-Z]{6}\d{2}[A-Z]\d{2}[A-Z]\d{3}[A-Z]\b', text, re.IGNORECASE)
        pii.update(cf_matches)

        # Carte di Credito (16 cifre formattate o meno)
        cc_matches = re.findall(r'\b(?:\d[ -]*?){13,16}\b', text)
        for cc in cc_matches:
            clean_cc = cc.replace(" ", "").replace("-", "")
            if len(clean_cc) == 16 and clean_cc.isdigit():
                pii.add(cc)

        # IBAN
        iban_matches = re.findall(r'\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b', text, re.IGNORECASE)
        pii.update(iban_matches)

        # Extraction via spaCy NER (se caricato)
        if self.nlp:
            doc = self.nlp(text)
            for ent in doc.ents:
                if ent.label_ in ["PERSON", "ORG", "GPE"]:
                    pii.add(ent.text)

        return list(pii)

    def purge_user(self, target_name: str, dry_run: bool = False) -> Dict[str, Any]:
        docs = self.adapter.fetch_all_documents()
        variants = self.generate_name_variants(target_name)
        
        ids_to_purge = []
        secondary_pii = set()

        # Phase 1: Identificazione diretta e estrazione PII estesa
        for doc in docs:
            text = doc['text']
            matched = any(re.search(rf"\b{re.escape(v)}\b", text, re.IGNORECASE) for v in variants)
            
            if matched:
                ids_to_purge.append(doc['id'])
                extracted = self.extract_pii_from_text(text)
                secondary_pii.update(extracted)

        # Rimuoviamo il nome target, le sue varianti e le stringhe che lo contengono per evitare falsi positivi
        cleaned_pii = set()
        for pii_item in secondary_pii:
            # Se la PII estratta contiene il nome target o una sua variante, non la usiamo come PII secondaria
            if any(v.lower() in pii_item.lower() for v in variants):
                continue
            cleaned_pii.add(pii_item)
        
        secondary_pii = cleaned_pii
        # Phase 2: Cascading Purge per vettori orfani
        if secondary_pii:
            for doc in docs:
                if doc['id'] in ids_to_purge:
                    continue
                text = doc['text']
                if any(pii in text for pii in secondary_pii):
                    ids_to_purge.append(doc['id'])

        if dry_run:
            return {
                "status": "SIMULATION_SUCCESSFUL",
                "dry_run": True,
                "db_name": self.db_name,
                "target_name": target_name,
                "vector_ids_to_be_purged": ids_to_purge,
                "secondary_pii_extracted": list(secondary_pii),
                "total_vectors_affected": len(ids_to_purge)
            }

        deleted_count = self.adapter.delete_documents_by_ids(ids_to_purge)

        audit_certificate = self.auditor.log_purge(
            db_name=self.db_name,
            target_name=target_name,
            purged_ids=ids_to_purge,
            secondary_pii_found=list(secondary_pii)
        )

        return audit_certificate