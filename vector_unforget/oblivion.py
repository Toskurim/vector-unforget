"""
Zero-Config Oblivion: NLP & Heuristic Automatic PII/Concept Extraction for VectorUnforget.
"""

import re
from typing import List, Dict, Any, Optional
import numpy as np


class OblivionExtractor:
    """
    Automated zero-config extractor for PII entities, tokens, and concept directives.
    """

    DEFAULT_PATTERNS = {
        "EMAIL": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
        "PHONE": r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
        "TAX_ID": r"\b[A-Z]{6}[0-9]{2}[A-Z][0-9]{2}[A-Z][0-9]{3}[A-Z]\b",
        "CREDIT_CARD": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
        "IP_ADDRESS": r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
    }

    ACTION_TRIGGERS = [
        r"dimentica\s+(?:tutto\s+su\s+|le\s+informazioni\s+di\s+|i\s+dati\s+di\s+)?(.+)",
        r"forget\s+(?:everything\s+about\s+|all\s+data\s+for\s+|records\s+of\s+)?(.+)",
        r"erase\s+(?:pii\s+for\s+|identity\s+of\s+)?(.+)",
        r"purge\s+(.+)"
    ]

    def __init__(self, custom_patterns: Optional[Dict[str, str]] = None):
        self.patterns = dict(self.DEFAULT_PATTERNS)
        if custom_patterns:
            self.patterns.update(custom_patterns)

    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract structured PII entities matching known regulatory and structural patterns.
        """
        results: Dict[str, List[str]] = {}
        for category, pattern in self.patterns.items():
            matches = re.findall(pattern, text, flags=re.IGNORECASE)
            if matches:
                results[category] = list(set(matches))
        return results

    def parse_intent(self, prompt: str) -> Dict[str, Any]:
        """
        Parse natural language erasure commands into target entities and action scopes.
        """
        clean_prompt = prompt.strip()
        target_concept = None

        for trigger in self.ACTION_TRIGGERS:
            match = re.search(trigger, clean_prompt, flags=re.IGNORECASE)
            if match:
                target_concept = match.group(1).strip(" .?!;:")
                break

        if not target_concept:
            target_concept = clean_prompt

        entities = self.extract_entities(clean_prompt)
        
        all_terms = set()
        if target_concept:
            all_terms.add(target_concept.lower())
        for term_list in entities.values():
            for t in term_list:
                all_terms.add(t.lower())

        return {
            "target_concept": target_concept,
            "detected_pii": entities,
            "seed_terms": list(all_terms)
        }

    def generate_synthetic_concept_vector(self, terms: List[str], dim: int = 768, seed: Optional[int] = None) -> np.ndarray:
        """
        Deterministic centroid embedding generator for lightweight/zero-dependency deployments.
        """
        if seed is None:
            combined_hash = sum(sum(ord(c) for c in t) for t in terms) if terms else 42
            seed = combined_hash % (2**32)
            
        rng = np.random.RandomState(seed)
        vec = rng.randn(dim).astype(np.float32)
        norm = np.linalg.norm(vec)
        return vec / (norm + 1e-12)
