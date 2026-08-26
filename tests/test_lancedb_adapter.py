"""
Tests for LanceDB Adapter.
"""

from unittest.mock import MagicMock
from vector_unforget.adapters.lancedb_adapter import LanceDBAdapter


def test_lancedb_delete():
    mock_table = MagicMock()
    mock_table.delete.return_value = None

    adapter = LanceDBAdapter(table=mock_table)
    res = adapter.delete_documents_by_ids(["lance_1", "lance_2"], dry_run=False)

    assert res["deleted_count"] == 2
    assert res["is_dry_run"] is False
    mock_table.delete.assert_called_once_with('id IN ("lance_1", "lance_2")')


def test_lancedb_dry_run():
    mock_table = MagicMock()
    adapter = LanceDBAdapter(table=mock_table)
    res = adapter.delete_documents_by_ids(["lance_1"], dry_run=True)

    assert res["deleted_count"] == 1
    assert res["is_dry_run"] is True
    mock_table.delete.assert_not_called()