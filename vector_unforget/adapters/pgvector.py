from typing import List, Dict, Any
from vector_unforget.adapters.base import BaseVectorAdapter

try:
    import psycopg
    from psycopg.rows import dict_row
except ImportError:
    psycopg = None

class PgvectorAdapter(BaseVectorAdapter):
    def __init__(self, connection_string: str, table_name: str, id_column: str = "id", text_column: str = "text"):
        if psycopg is None:
            raise ImportError("Installa psycopg eseguendo: pip install 'psycopg[binary]'")
        self.connection_string = connection_string
        self.table_name = table_name
        self.id_column = id_column
        self.text_column = text_column

    def fetch_all_documents(self) -> List[Dict[str, Any]]:
        documents = []
        with psycopg.connect(self.connection_string, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                query = f"SELECT {self.id_column}, {self.text_column} FROM {self.table_name};"
                cur.execute(query)
                rows = cur.fetchall()
                for row in rows:
                    documents.append({
                        'id': str(row[self.id_column]),
                        'text': row[self.text_column] or "",
                        'metadata': {}
                    })
        return documents

    def delete_documents_by_ids(self, ids: List[str]) -> int:
        if not ids:
            return 0
        with psycopg.connect(self.connection_string) as conn:
            with conn.cursor() as cur:
                # Utilizziamo la clausola WHERE id = ANY(%s) per una cancellazione sicura
                query = f"DELETE FROM {self.table_name} WHERE {self.id_column}::text = ANY(%s);"
                cur.execute(query, (ids,))
                conn.commit()
                return cur.rowcount