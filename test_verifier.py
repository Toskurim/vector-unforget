"""
Test Suite: Reverse RAG Verification Engine.
Author: Toskurim
"""

from vector_unforget.verifier import ReverseRAGVerifier


class MockAdapterClean:
    """Simulates a database after complete and successful erasure."""
    def query_text(self, query: str, limit: int = 10):
        return [
            {"id": "vec-101", "text": "Unrelated mechanical component catalog for CNC tooling."},
            {"id": "vec-102", "text": "General maintenance logs for warehouse operations."},
        ]


class MockAdapterLeaking:
    """Simulates a database with residual orphaned PII chunks."""
    def query_text(self, query: str, limit: int = 10):
        if "123-45-6789" in query:
            return [{"id": "vec-999", "text": "Orphaned backup entry containing SSN: 123-45-6789."}]
        return []


def test_reverse_rag_clean_verification():
    adapter = MockAdapterClean()
    verifier = ReverseRAGVerifier(adapter)

    report = verifier.verify_erasure(
        target_name="John Doe",
        extracted_pii={"123-45-6789", "john.doe@example.com"},
    )

    assert report["is_fully_compliant"] is True
    assert report["zero_residual_leakage_score"] == 100.0
    assert report["leakage_incidents"] == 0


def test_reverse_rag_detects_leakage():
    adapter = MockAdapterLeaking()
    verifier = ReverseRAGVerifier(adapter)

    report = verifier.verify_erasure(
        target_name="John Doe",
        extracted_pii={"123-45-6789"},
    )

    assert report["is_fully_compliant"] is False
    assert report["zero_residual_leakage_score"] < 100.0
    assert report["leakage_incidents"] > 0
    assert report["incidents"][0]["vector_id"] == "vec-999"


if __name__ == "__main__":
    test_reverse_rag_clean_verification()
    test_reverse_rag_detects_leakage()
    print("✅ Reverse RAG Verifier tests passed successfully!")