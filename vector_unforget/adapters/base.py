from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseVectorAdapter(ABC):
    """
    Interfaccia astratta per uniformare la gestione dei vari Vector DB.
    """

    @abstractmethod
    def fetch_all_documents(self) -> List[Dict[str, Any]]:
        """
        Recupera tutti i documenti con id, payload/metadati e testo originale.
        Ritorna una lista di dizionari: [{'id': ..., 'text': ..., 'metadata': ...}]
        """
        pass

    @abstractmethod
    def delete_documents_by_ids(self, ids: List[str]) -> int:
        """
        Elimina i vettori corrispondenti alla lista di ID forniti.
        Ritorna il numero di elementi eliminati.
        """
        pass