from vector_unforget.metrics import MetricsTracker
from fastapi.testclient import TestClient
from vector_unforget.api.server import create_app


def test_metrics_tracker_unit():
    tracker = MetricsTracker()
    tracker.record_unlearn(count=100, latency=0.0042)
    tracker.record_graph_resolve(nodes_count=8)
    tracker.record_certificate(leakage_score=0.001)

    payload = tracker.generate_prometheus_payload()
    assert "vector_unforget_unlearned_vectors_total 100" in payload
    assert "vector_unforget_cascading_nodes_total 8" in payload
    assert "vector_unforget_certificates_total 1" in payload
    assert "vector_unforget_last_leakage_score 0.001" in payload


def test_prometheus_endpoint():
    app = create_app()
    client = TestClient(app)

    # Trigger a batch unlearn to increment metrics
    client.post("/v1/unlearn/batch", json={
        "embeddings": [[1.0, 0.0], [0.0, 1.0]],
        "concept_vector": [1.0, 0.0]
    })

    response = client.get("/metrics")
    assert response.status_code == 200
    assert "vector_unforget_unlearned_vectors_total" in response.text
    assert "# TYPE vector_unforget_unlearned_vectors_total counter" in response.text
