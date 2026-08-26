from unittest.mock import MagicMock
from vector_unforget.adapters.elasticsearch_adapter import ElasticsearchAdapter


def test_elasticsearch_adapter_dry_run():
    mock_client = MagicMock()
    adapter = ElasticsearchAdapter(client=mock_client, index="test_index")

    res = adapter.delete_documents_by_ids(["doc_1", "doc_2"], dry_run=True)
    assert res["status"] == "dry_run_success"
    assert res["deleted_count"] == 2
    mock_client.delete_by_query.assert_not_called()


def test_elasticsearch_adapter_execution():
    mock_client = MagicMock()
    mock_client.delete_by_query.return_value = {"deleted": 2}

    adapter = ElasticsearchAdapter(client=mock_client, index="test_index")
    res = adapter.delete_documents_by_ids(["es_1", "es_2"], dry_run=False)

    assert res["status"] == "success"
    assert res["deleted_count"] == 2
    mock_client.delete_by_query.assert_called_once_with(
        index="test_index",
        query={"ids": {"values": ["es_1", "es_2"]}}
    )


def test_elasticsearch_fetch_documents():
    mock_client = MagicMock()
    mock_client.search.return_value = {
        "hits": {
            "hits": [
                {"_id": "doc1", "_source": {"text": "Alice secret", "vector": [0.1, 0.2], "group": "hr"}},
                {"_id": "doc2", "_source": {"text": "Bob public", "vector": [0.3, 0.4], "group": "eng"}},
            ]
        }
    }

    adapter = ElasticsearchAdapter(client=mock_client, index="test_index")
    docs = adapter.fetch_all_documents(limit=10)

    assert len(docs) == 2
    assert docs[0]["id"] == "doc1"
    assert docs[0]["text"] == "Alice secret"
    assert docs[0]["vector"] == [0.1, 0.2]
    assert docs[0]["metadata"] == {"group": "hr"}