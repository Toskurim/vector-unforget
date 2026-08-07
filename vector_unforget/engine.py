from typing import List, Dict, Any, Optional
import re
import spacy
from vector_unforget.adapters.base import BaseVectorAdapter
from vector_unforget.auditor import AuditLogger

class VectorUnforgetEngine:
    def __init__(
        self, 
        adapter: BaseVectorAdapter, 
        db_name: str = "vector_db",
        spacy_model: str = "en_core_web_sm"
    ):
        self.adapter = adapter
        self.db_name = db_name
        self.spacy_model_name = spacy_model
        try:
            self.nlp = spacy.load(spacy_model)
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
        
        # 1. GLOBAL PII (Universali)
        # Email
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
        pii.update(emails)

        # Telefoni Internazionali (formato E.164 e varianti)
        phones = re.findall(r'\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}', text)
        for ph in phones:
            clean_ph = re.sub(r'[^\d+]', '', ph)
            if len(clean_ph) >= 9:
                pii.add(ph)

        # Carte di Credito (Visa, MasterCard, Amex, ecc.)
        cc_matches = re.findall(r'\b(?:\d[ -]*?){13,16}\b', text)
        for cc in cc_matches:
            clean_cc = cc.replace(" ", "").replace("-", "")
            if 13 <= len(clean_cc) <= 16 and clean_cc.isdigit():
                pii.add(cc)

        # IBAN Internazionale
        iban_matches = re.findall(r'\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b', text, re.IGNORECASE)
        pii.update(iban_matches)

        # Indirizzi IPv4 e IPv6
        ipv4_matches = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', text)
        pii.update(ipv4_matches)

        # 2. NATIONAL IDENTIFIERS (Codici Nazionali)
        # USA: Social Security Number (SSN) -> XXX-XX-XXXX
        ssn_matches = re.findall(r'\b(?!000|666|9\d{2})\d{3}-(?!00)\d{2}-(?!0000)\d{4}\b', text)
        pii.update(ssn_matches)

        # UK: National Insurance Number (NINO) -> QQ123456C
        nino_matches = re.findall(r'\b[A-CEGHJ-PR-TW-Z]{1}[A-CEGHJ-NPR-TW-Z]{1}[0-9]{6}[A-D]{1}\b', text, re.IGNORECASE)
        pii.update(nino_matches)

        # ITALIA: Codice Fiscale
        cf_matches = re.findall(r'\b[A-Z]{6}\d{2}[A-Z]\d{2}[A-Z]\d{3}[A-Z]\b', text, re.IGNORECASE)
        pii.update(cf_matches)

        # CANADA: Social Insurance Number (SIN) -> XXX-XXX-XXX
        sin_matches = re.findall(r'\b\d{3}-\d{3}-\d{3}\b', text)
        pii.update(sin_matches)

        # GERMANIA: Steuerliche Identifikationsnummer (Steuer-ID) -> 11 cifre
        steuer_matches = re.findall(r'\b\d{11}\b', text)
        # Nota: usiamo Steuer-ID solo se non è un numero di telefono o carta
        for st in steuer_matches:
            if not any(st in cc for cc in pii):
                pii.add(st)

        # 3. MULTILINGUAL NER (spaCy)
        if self.nlp:
            doc = self.nlp(text)
            for ent in doc.ents:
                # PERSON, ORG, GPE (Località), FAC (Infrastrutture/Indirizzi)
                if ent.label_ in ["PERSON", "ORG", "GPE", "FAC"]:
                    pii.add(ent.text)

        return list(pii)

    def purge_user(self, target_name: str, dry_run: bool = False) -> Dict[str, Any]:
        docs = self.adapter.fetch_all_documents()
        variants = self.generate_name_variants(target_name)
        
        ids_to_purge = []
        secondary_pii = set()

        # Phase 1: Identificazione diretta e estrazione PII
        for doc in docs:
            text = doc['text']
            matched = any(re.search(rf"\b{re.escape(v)}\b", text, re.IGNORECASE) for v in variants)
            
            if matched:
                ids_to_purge.append(doc['id'])
                extracted = self.extract_pii_from_text(text)
                secondary_pii.update(extracted)

        # Pulizia PII: rimuoviamo stringhe che contengono il nome target o varianti
        cleaned_pii = set()
        for pii_item in secondary_pii:
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
                "spacy_model_used": self.spacy_model_name,
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