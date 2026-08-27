import numpy as np
from vector_unforget.adapters.qdrant_adapter import QdrantAdapter
from vector_unforget.adapters.chroma_adapter import ChromaAdapter


class MockQdrantPoint:
    def __init__(self, pid, vector):
        self.id = pid
        self.vector = vector


class MockQdrantClient:
    def __init__(self):
        self.storage = {
            "p1": [1.0, 0.0, 0.0],
            "p2": [0.0, 1.0, 0.0]
        }

    def scroll(self, collection_name, limit, with_vectors):
        pts = [MockQdrantPoint(k, v) for k, v in self.storage.items()][:limit]
        return pts, None

    def update_vectors(self, collection_name, points):
        return True

    def delete(self, collection_name, points_selector):
        return True


class MockChromaCollection:
    def __init__(self):
        self.data = {
            "ids": ["c1", "c2"],
            "embeddings": [[0.5, 0.5], [0.1, 0.9]]
        }

    def get(self, include, limit):
        return {
            "ids": self.data["ids"][:limit],
            "embeddings": self.data["embeddings"][:limit]
        }

    def update(self, ids, embeddings):
        return True

    def delete(self, ids):
        return True


def test_qdrant_adapter_flow():
    client = MockQdrantClient()
    adapter = QdrantAdapter(client=client, collection_name="test_col")
    data = adapter.fetch_embeddings(limit=10)
    assert len(data) == 2
    assert "p1" in data
    assert isinstance(data["p1"], np.ndarray)
    assert adapter.update_embeddings(data) is True
    assert adapter.delete_by_ids(["p1"]) is True


def test_chroma_adapter_flow():
    coll = MockChromaCollection()
    adapter = ChromaAdapter(collection=coll)
    data = adapter.fetch_embeddings(limit=10)
    assert len(data) == 2
    assert "c1" in data
    assert isinstance(data["c1"], np.ndarray)
    assert adapter.update_embeddings(data) is True
    assert adapter.delete_by_ids(["c1"]) is True
