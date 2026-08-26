"""
Tests for Weaviate Adapter.
"""

from unittest.mock import MagicMock
from vector_unforget.adapters.weaviate import WeaviateAdapter


def test_weaviate_delete_records():
    mock_client = MagicMock()
    adapter = WeaviateAdapter(client=mock_client, class_name="Document")
    res = adapter.delete_documents_by_ids(["uuid-1", "uuid-2"])

    assert res is True


def test_weaviate_empty_delete():
    mock_client = MagicMock()
    adapter = WeaviateAdapter(client=mock_client, class_name="Document")
    res = adapter.delete_documents_by_ids([])

    assert res is True