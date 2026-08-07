from typing import List, Dict, Any
from vector_unforget.adapters.base import BaseVectorAdapter

try:
    from qdrant_client import QdrantClient
    from qdrant_client.http import models
except ImportError:
    QdrantClient = None

class QdrantAdapter(BaseVectorAdapter):
    def __init__(self, client, collection_name: str, text_field: str = "text"):
        if QdrantClient is None:
            raise ImportError("Installa qdrant-client eseguendo: pip install qdrant-client")
        self.client = client
        self.collection_name = collection_name
        self.text_field = text_field

    def fetch_all_documents(self) -> List[Dict[str, Any]]:
        records, _ = self.client.scroll(
            collection_name=self.collection_name,
            limit=10000,
            with_payload=True,
            with_vectors=False
        )
        
        documents = []
        for record in records:
            payload = record.payload or {}
            text = payload.get(self.text_field, "")
            documents.append({
                'id': str(record.id),
                'text': text,
                'metadata': payload
            })
        return documents

    def delete_documents_by_ids(self, ids: List[str]) -> int:
        if not ids:
            return 0
        
        # Converte in int gli ID se sono numerici (per compatibilità con Qdrant)
        parsed_ids = []
        for i in ids:
            if isinstance(i, str) and i.isdigit():
                parsed_ids.append(int(i))
            else:
                parsed_ids.append(i)

        self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.PointIdsList(points=parsed_ids)
        )
        return len(ids)