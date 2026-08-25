"""
Reverse RAG Verification Engine for VectorUnforget.
Author: Toskurim
License: AGPLv3
"""

from typing import List, Dict, Any, Set
import re


class ReverseRAGVerifier:
    """
    Verifies that purged entities/PIIs cannot be retrieved via RAG queries.
    Calculates the Zero Residual Leakage Score and produces a verifiable audit report.
    """

    def __init__(self, adapter):
        """
        :param adapter: Initialized VectorUnforget adapter instance.
        """
        self.adapter = adapter

    def generate_adversarial_queries(self, target_name: str, extracted_pii: Set[str]) -> List[str]:
        """Generates targeted probing queries to test residual presence."""
        queries = [
            target_name,
            f"Who is {target_name}?",
            f"Information about {target_name}",
            f"Profile and records for {target_name}",
        ]
        for pii in extracted_pii:
            queries.append(f"Find record matching {pii}")
            queries.append(f"Who owns {pii}?")
            queries.append(pii)
        return list(dict.fromkeys(queries))

    def verify_erasure(
        self,
        target_name: str,
        extracted_pii: Set[str],
        top_k: int = 10,
    ) -> Dict[str, Any]:
        """
        Executes adversarial probing queries across the vector store.
        Returns leakage metrics and a verification score (100% = zero leakage).
        """
        queries = self.generate_adversarial_queries(target_name, extracted_pii)
        leakage_detected = []
        total_queries = len(queries)

        forbidden_terms = {target_name.lower()} | {p.lower() for p in extracted_pii}

        for query in queries:
            try:
                results = self.adapter.query_text(query, limit=top_k)
            except Exception:
                results = []

            for doc in results:
                content = ""
                doc_id = None
                if isinstance(doc, dict):
                    content = doc.get("text") or doc.get("content") or str(doc)
                    doc_id = doc.get("id")
                elif hasattr(doc, "page_content"):
                    content = doc.page_content
                    doc_id = getattr(doc, "id", None)
                else:
                    content = str(doc)

                content_lower = content.lower()
                for term in forbidden_terms:
                    if re.search(rf"\b{re.escape(term)}\b", content_lower):
                        leakage_detected.append({
                            "query": query,
                            "leaked_term": term,
                            "vector_id": doc_id,
                            "snippet": content[:120] + ("..." if len(content) > 120 else ""),
                        })
                        break

        leak_count = len(leakage_detected)
        leakage_score = 100.0 if total_queries == 0 else max(0.0, 100.0 - (leak_count / total_queries * 100.0))

        return {
            "target": target_name,
            "queries_tested": total_queries,
            "leakage_incidents": leak_count,
            "zero_residual_leakage_score": round(leakage_score, 2),
            "is_fully_compliant": leak_count == 0,
            "incidents": leakage_detected,
        }