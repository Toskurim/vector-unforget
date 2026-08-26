import numpy as np
from vector_unforget.hybrid_scrubber import HybridSearchScrubber


def test_hybrid_text_token_scrubbing():
    scrubber = HybridSearchScrubber()
    raw_text = "Alice Cooper lives in Milan and works at Meccanica Broter."
    sensitive_terms = {"Alice Cooper", "Milan"}

    sanitized = scrubber.scrub_text_tokens(raw_text, sensitive_terms)
    assert "Alice Cooper" not in sanitized
    assert "Milan" not in sanitized
    assert "[REDACTED] lives in [REDACTED] and works at Meccanica Broter." == sanitized


def test_dual_phase_hybrid_document_processing():
    scrubber = HybridSearchScrubber()
    doc_text = "Confidential report for Project Titan."
    embedding = np.array([1.0, 1.0, 0.0], dtype=np.float32)
    concept_vector = np.array([1.0, 0.0, 0.0], dtype=np.float32)
    sensitive_terms = {"Project Titan"}

    result = scrubber.process_hybrid_document(
        doc_text=doc_text,
        embedding=embedding,
        concept_vector=concept_vector,
        sensitive_terms=sensitive_terms,
        normalize=True
    )

    assert "Project Titan" not in result["sanitized_text"]
    assert "[REDACTED]" in result["sanitized_text"]
    # Verifica ortogonalità del vettore risultante
    assert abs(np.dot(result["unlearned_vector"], concept_vector)) < 1e-6
    assert abs(np.linalg.norm(result["unlearned_vector"]) - 1.0) < 1e-6