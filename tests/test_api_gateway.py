import pytest
from fastapi.testclient import TestClient
from vector_unforget.api.server import create_app


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_unlearn_batch_endpoint(client):
    payload = {
        "embeddings": [
            [1.0, 1.0, 0.0],
            [0.0, 2.0, 0.0]
        ],
        "concept_vector": [1.0, 0.0, 0.0],
        "normalize": True
    }
    response = client.post("/v1/unlearn/batch", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["vector_count"] == 2
    # Verify orthogonalization
    for vec in data["unlearned_embeddings"]:
        dot_c = vec[0] * 1.0 + vec[1] * 0.0 + vec[2] * 0.0
        assert abs(dot_c) < 1e-5


def test_audit_verify_endpoint(client):
    payload = {
        "query_vector": [1.0, 0.0],
        "retrieved_vectors": [
            [0.0, 1.0],
            [0.0, -1.0]
        ],
        "threshold": 0.1
    }
    response = client.post("/v1/audit/verify", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["passed"] is True
    assert data["max_similarity"] < 0.1