"""
LanceDB Adapter for VectorUnforget.
Author: Toskurim
License: AGPLv3
"""

from typing import List, Dict, Any
from vector_unforget.adapters.base import BaseVectorAdapter


class LanceDBAdapter(BaseVectorAdapter):
    """
    Adapter for LanceDB embedded/serverless vector tables.
    """

    def __init__(self, table: Any):
        self.table = table

    def fetch_all_documents(self) -> List[Dict[str, Any]]:
        try:
            results = self.table.to_pandas().to_dict(orient="records")
            return [
                {
                    "id": str(r.get("id", "")),
                    "text": str(r.get("text", "")),
                    "metadata": {k: v for k, v in r.items() if k not in ("id", "text", "vector")},
                }
                for r in results
            ]
        except Exception:
            return []

    def delete_documents_by_ids(self, ids: List[str], dry_run: bool = False) -> Dict[str, Any]:
        if not ids:
            return {"deleted_count": 0, "is_dry_run": dry_run}

        if dry_run:
            return {"deleted_count": len(ids), "is_dry_run": True}

        try:
            formatted_ids = ", ".join(f'"{i}"' for i in ids)
            filter_query = f"id IN ({formatted_ids})"
            self.table.delete(filter_query)
            return {"deleted_count": len(ids), "is_dry_run": False}
        except Exception:
            return {"deleted_count": 0, "is_dry_run": False}