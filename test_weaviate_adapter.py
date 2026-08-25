"""
Test Suite: Weaviate Adapter Integration.
Author: Toskurim
"""

from vector_unforget.adapters.weaviate import WeaviateAdapter


class MockWeaviateClient:
    def __init__(self):
        self.records = [
            {"id": "weav-1", "properties": {"text": "Confidential patient file for Dr. Rossi, tax code: RSSMRA85M01H501Z"}},
            {"id": "weav-2", "properties": {"text": "Public API documentation for vector embedding endpoints."}},
            {"id": "weav-3", "properties": {"text": "Access log entry originating from IP 192.168.0.22"}},
        ]
        self.deleted_ids = []

    def delete_records(self, ids):
        self.deleted_ids.extend(ids)
        self.records = [r for r in self.records if r["id"] not in ids]


def test_weaviate_scan_and_dry_run():
    mock_client = MockWeaviateClient()
    adapter = WeaviateAdapter(client=mock_client, class_name="Document")

    matches = adapter.find_records_by_terms(["RSSMRA85M01H501Z", "192.168.0.22"])
    ids = [m["id"] for m in matches]
    assert len(ids) == 2
    assert "weav-1" in ids
    assert "weav-3" in ids

    # Dry-run
    dry_result = adapter.delete_records(ids, dry_run=True)
    assert dry_result["status"] == "simulated"
    assert dry_result["deleted_count"] == 2
    assert len(mock_client.deleted_ids) == 0


def test_weaviate_real_deletion():
    mock_client = MockWeaviateClient()
    adapter = WeaviateAdapter(client=mock_client, class_name="Document")

    real_result = adapter.delete_records(["weav-1"], dry_run=False)
    assert real_result["status"] == "success"
    assert "weav-1" in mock_client.deleted_ids
    assert len(mock_client.records) == 2


if __name__ == "__main__":
    test_weaviate_scan_and_dry_run()
    test_weaviate_real_deletion()
    print("✅ Weaviate Adapter tests passed successfully!")