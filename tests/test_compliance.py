from vector_unforget.compliance import ComplianceCertificateGenerator
from fastapi.testclient import TestClient
from vector_unforget.api.server import create_app


def test_certificate_generator_logic():
    generator = ComplianceCertificateGenerator()
    cert = generator.generate_certificate(
        request_id="REQ-9921",
        entity_identifier="user_12345",
        unlearned_vector_count=15,
        pre_unlearning_leakage=0.82,
        post_unlearning_leakage=0.01,
        scrubbed_terms=["John Doe", "Milan"],
        regulation="GDPR_Art_17"
    )

    assert cert["request_id"] == "REQ-9921"
    assert cert["target_entity"] == "user_12345"
    assert cert["unlearned_vector_count"] == 15
    assert cert["metrics"]["zero_residual_leakage_verified"] is True
    assert len(cert["cryptographic_hash_sha256"]) == 64


def test_certificate_rest_endpoint():
    app = create_app()
    client = TestClient(app)

    payload = {
        "request_id": "GDPR-2026-001",
        "entity_identifier": "entity_abc",
        "unlearned_vector_count": 5,
        "pre_leakage_score": 0.75,
        "post_leakage_score": 0.02,
        "scrubbed_terms": ["Secret Alpha"]
    }
    response = client.post("/v1/audit/certificate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "cryptographic_hash_sha256" in data["certificate"]
    assert data["certificate"]["metrics"]["semantic_attenuation_delta"] == 0.73
