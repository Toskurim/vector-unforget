"""
Tests for Pinecone Adapter.
"""

from unittest.mock import MagicMock
from vector_unforget.adapters.pinecone import PineconeAdapter


def test_pinecone_delete_records():
    mock_index = MagicMock()
    mock_index.delete.return_value = None

    adapter = PineconeAdapter(index=mock_index, namespace="test-ns")
    res = adapter.delete_documents_by_ids(["vec-1", "vec-2"])

    assert res is True
    mock_index.delete.assert_called_once_with(ids=["vec-1", "vec-2"], namespace="test-ns")


def test_pinecone_empty_delete():
    mock_index = MagicMock()
    adapter = PineconeAdapter(index=mock_index, namespace="test-ns")
    res = adapter.delete_documents_by_ids([])

    assert res is True
    mock_index.delete.assert_not_called()