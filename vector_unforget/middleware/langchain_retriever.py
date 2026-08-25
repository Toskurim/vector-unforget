"""
VectorUnforget Middleware: LangChain Retriever Wrapper.
Author: Toskurim
License: AGPLv3
"""

from typing import List, Optional, Set
import re


class VectorUnforgetRetriever:
    """
    Wraps any standard retriever or document list, enforcing real-time 
    compliance by filtering out documents belonging to forgotten entities/PIIs.
    """

    def __init__(
        self,
        base_retriever=None,
        blocked_identifiers: Optional[Set[str]] = None,
    ):
        """
        :param base_retriever: An underlying LangChain BaseRetriever or callable.
        :param blocked_identifiers: Set of strings, PII, names, or IDs that must never be returned.
        """
        self.base_retriever = base_retriever
        self.blocked_identifiers = set(blocked_identifiers) if blocked_identifiers else set()

    def add_blocked_identifier(self, identifier: str) -> None:
        """Dynamically add an identifier (name, email, SSN, IP) to block."""
        if identifier:
            self.blocked_identifiers.add(identifier.strip().lower())

    def remove_blocked_identifier(self, identifier: str) -> None:
        """Remove an identifier from the blocklist."""
        clean = identifier.strip().lower()
        if clean in self.blocked_identifiers:
            self.blocked_identifiers.remove(clean)

    def is_compliant(self, text: str) -> bool:
        """
        Checks whether the given text contains any forbidden identifier.
        Returns False if text contains blocked PII/names, True otherwise.
        """
        if not self.blocked_identifiers or not text:
            return True

        text_lower = text.lower()
        for blocked in self.blocked_identifiers:
            if re.search(rf"\b{re.escape(blocked)}\b", text_lower):
                return False
        return True

    def filter_documents(self, documents: List[any]) -> List[any]:
        """
        Filters a list of documents (LangChain Document objects or strings/dicts).
        """
        clean_docs = []
        for doc in documents:
            content = ""
            if hasattr(doc, "page_content"):
                content = doc.page_content
            elif isinstance(doc, dict):
                content = doc.get("page_content") or doc.get("text") or str(doc)
            elif isinstance(doc, str):
                content = doc
            else:
                content = str(doc)

            if self.is_compliant(content):
                clean_docs.append(doc)
        return clean_docs

    def invoke(self, query: str, **kwargs) -> List[any]:
        """
        Standard LangChain invoke interface.
        Retrieves documents from the underlying retriever and purges non-compliant entries.
        """
        if self.base_retriever is None:
            return []

        if hasattr(self.base_retriever, "invoke"):
            raw_docs = self.base_retriever.invoke(query, **kwargs)
        elif hasattr(self.base_retriever, "get_relevant_documents"):
            raw_docs = self.base_retriever.get_relevant_documents(query, **kwargs)
        elif callable(self.base_retriever):
            raw_docs = self.base_retriever(query)
        else:
            raw_docs = []

        return self.filter_documents(raw_docs)