from unittest.mock import MagicMock
from vector_unforget.adapters.milvus_adapter import MilvusAdapter


def test_milvus_adapter_dry_run():
    mock_collection = MagicMock()
    adapter = MilvusAdapter(collection=mock_collection, pk_field="doc_id")

    res = adapter.delete_documents_by_ids(["doc_1", "doc_2"], dry_run=True)
    assert res["status"] == "dry_run_success"
    assert res["deleted_count"] == 2
    mock_collection.delete.assert_not_called()


def test_milvus_adapter_execution():
    mock_collection = MagicMock()
    mock_result = MagicMock()
    mock_result.delete_count = 2
    mock_collection.delete.return_value = mock_result

    adapter = MilvusAdapter(collection=mock_collection, pk_field="entity_id")
    res = adapter.delete_documents_by_ids(["e_100", "e_200"], dry_run=False)

    assert res["status"] == "success"
    assert res["deleted_count"] == 2
    mock_collection.delete.assert_called_once_with('entity_id in ["e_100", "e_200"]')