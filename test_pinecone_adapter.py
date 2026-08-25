"""
Test Suite: Pinecone Adapter Integration.
Author: Toskurim
"""

from vector_unforget.adapters.pinecone import PineconeAdapter


class MockPineconeIndex:
    def __init__(self):
        self.records = [
            {"id": "vec-1", "metadata": {"text": "User profile for Alice, email: alice@example.com"}},
            {"id": "vec-2", "metadata": {"text": "General CNC machine parameters and blueprints."}},
            {"id": "vec-3", "metadata": {"text": "Log transaction linked to IP 192.168.1.150"}},
        ]
        self.deleted_ids = []

    def scan_records(self, namespace=""):
        return self.records

    def delete(self, ids, namespace=""):
        self.deleted_ids.extend(ids)
        self.records = [r for r in self.records if r["id"] not in ids]


def test_pinecone_find_and_dry_run():
    mock_index = MockPineconeIndex()
    adapter = PineconeAdapter(mock_index)

    # 1. Search targets
    matches = adapter.find_records_by_terms(["alice@example.com", "192.168.1.150"])
    target_ids = [m["id"] for m in matches]
    assert len(target_ids) == 2
    assert "vec-1" in target_ids
    assert "vec-3" in target_ids

    # 2. Dry-Run Deletion
    dry_result = adapter.delete_records(target_ids, dry_run=True)
    assert dry_result["status"] == "simulated"
    assert dry_result["deleted_count"] == 2
    assert len(mock_index.deleted_ids) == 0  # Nothing actually deleted


def test_pinecone_real_deletion():
    mock_index = MockPineconeIndex()
    adapter = PineconeAdapter(mock_index)

    # Real Delete
    real_result = adapter.delete_records(["vec-1"], dry_run=False)
    assert real_result["status"] == "success"
    assert "vec-1" in mock_index.deleted_ids
    assert len(mock_index.records) == 2


if __name__ == "__main__":
    test_pinecone_find_and_dry_run()
    test_pinecone_real_deletion()
    print("✅ Pinecone Adapter tests passed successfully!")