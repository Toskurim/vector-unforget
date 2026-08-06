import re
from presidio_analyzer import AnalyzerEngine
from auditor import GDPRLogAuditor

class VectorUnforgetEngine:
    def __init__(self, collection, db_name="vector_db", log_file="gdpr_deletion_audit.json"):
        self.collection = collection
        self.db_name = db_name
        self.analyzer = AnalyzerEngine()
        self.auditor = GDPRLogAuditor(log_file=log_file)

    def _generate_aliases(self, full_name: str) -> list:
        parts = full_name.split()
        aliases = [full_name]
        if len(parts) >= 2:
            first, last = parts[0], parts[-1]
            aliases.extend([f"{first[0]}. {last}", f"{last} {first[0]}.", last])
        return aliases

    def _extract_pii_entities(self, text_list: list) -> set:
        """Estrae email, telefoni e altre PII trovate nei testi identificati"""
        extracted_pii = set()
        for text in text_list:
            results = self.analyzer.analyze(text=text, language="en")
            for res in results:
                entity_text = text[res.start:res.end]
                # Salviamo solo PII specifiche come e-mail e numeri di telefono
                if res.entity_type in ["EMAIL_ADDRESS", "PHONE_NUMBER"]:
                    extracted_pii.add(entity_text)
        return extracted_pii

    def purge_user(self, user_name: str) -> dict:
        print(f"\n--- Avvio Purge Engine a Cascata per: '{user_name}' ---")
        aliases = self._generate_aliases(user_name)
        
        results = self.collection.get()
        all_docs = results['documents']
        all_ids = results['ids']
        
        matched_ids = set()
        matched_texts = []

        # PASSAGGIO 1: Scansione per Nome e Alias
        for doc_id, text in zip(all_ids, all_docs):
            for alias in aliases:
                pattern = re.compile(r'\b' + re.escape(alias) + r'\b', re.IGNORECASE)
                if pattern.search(text):
                    matched_ids.add(doc_id)
                    matched_texts.append(text)
                    break

        # PASSAGGIO 2: Estrazione PII dai documenti trovati
        secondary_pii = self._extract_pii_entities(matched_texts)
        if secondary_pii:
            print(f"[PII CASCADING] Entità secondarie identificate per l'espansione: {secondary_pii}")

        # PASSAGGIO 3: Seconda scansione per le PII estratte (e-mail, telefoni)
        for doc_id, text in zip(all_ids, all_docs):
            if doc_id not in matched_ids:
                for pii in secondary_pii:
                    if pii.lower() in text.lower():
                        matched_ids.add(doc_id)
                        print(f"[MATCH CASCATA] Trovato recapito '{pii}' isolato in [{doc_id}]")
                        break

        # PASSAGGIO 4: Eliminazione e Registrazione Audit
        purged_list = sorted(list(matched_ids))
        if purged_list:
            self.collection.delete(ids=purged_list)
            print(f"[GDPR PURGE] Eliminati definitivamente {len(purged_list)} vettori.")
            return self.auditor.generate_proof(
                target_user=user_name, 
                purged_ids=purged_list, 
                db_name=self.db_name
            )
        else:
            print("Nessun dato identificato.")
            return {}