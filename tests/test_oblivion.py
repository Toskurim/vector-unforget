import pytest
import numpy as np
from vector_unforget.oblivion import OblivionExtractor


def test_extract_patterns():
    extractor = OblivionExtractor()
    sample = "Contatto mario.rossi@example.com, CF RSSMRA80A01H501U e IP 192.168.1.1."
    entities = extractor.extract_entities(sample)
    
    assert "EMAIL" in entities
    assert "mario.rossi@example.com" in entities["EMAIL"]
    assert "TAX_ID" in entities
    assert "RSSMRA80A01H501U" in entities["TAX_ID"]
    assert "IP_ADDRESS" in entities
    assert "192.168.1.1" in entities["IP_ADDRESS"]


def test_parse_intent_commands():
    extractor = OblivionExtractor()
    intent = extractor.parse_intent("Dimentica tutte le informazioni di Mario Rossi")
    assert intent["target_concept"].lower() == "mario rossi"
    assert "mario rossi" in intent["seed_terms"]


def test_deterministic_concept_vector():
    extractor = OblivionExtractor()
    v1 = extractor.generate_synthetic_concept_vector(["Mario Rossi", "RSSMRA80A01H501U"], dim=768)
    v2 = extractor.generate_synthetic_concept_vector(["Mario Rossi", "RSSMRA80A01H501U"], dim=768)
    
    assert v1.shape == (768,)
    assert np.allclose(v1, v2)
    assert np.isclose(np.linalg.norm(v1), 1.0, atol=1e-5)
