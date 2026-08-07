from typing import List, Dict, Any
from vector_unforget.adapters.base import BaseVectorAdapter

class ChromaAdapter(BaseVectorAdapter):
    def __init__(self, collection):
        self.collection = collection

    def fetch_all_documents(self) -> List[Dict[str, Any]]:
        results = self.collection.get()
        documents = []
        
        if not results or not results.get('ids'):
            return documents

        for idx, doc_id in enumerate(results['ids']):
            text = results['documents'][idx] if results.get('documents') else ""
            meta = results['metadatas'][idx] if results.get('metadatas') else {}
            documents.append({
                'id': doc_id,
                'text': text,
                'metadata': meta
            })
        return documents

    def delete_documents_by_ids(self, ids: List[str]) -> int:
        if not ids:
            return 0
        self.collection.delete(ids=ids)
        return len(ids)