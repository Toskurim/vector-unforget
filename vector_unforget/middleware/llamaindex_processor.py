"""
VectorUnforget Middleware: LlamaIndex Node Postprocessor.
Author: Toskurim
License: AGPLv3
"""

from typing import List, Optional, Set
import re


class VectorUnforgetNodePostprocessor:
    """
    LlamaIndex Node Postprocessor that enforces GDPR/CCPA compliance
    by filtering out retrieved nodes containing blocked identifiers or PII.
    """

    def __init__(self, blocked_identifiers: Optional[Set[str]] = None):
        """
        :param blocked_identifiers: Set of names, emails, SSNs, IPs, or IDs to block.
        """
        self.blocked_identifiers = set(blocked_identifiers) if blocked_identifiers else set()

    def add_blocked_identifier(self, identifier: str) -> None:
        """Add an identifier to the blocklist dynamically."""
        if identifier:
            self.blocked_identifiers.add(identifier.strip().lower())

    def remove_blocked_identifier(self, identifier: str) -> None:
        """Remove an identifier from the blocklist."""
        clean = identifier.strip().lower()
        if clean in self.blocked_identifiers:
            self.blocked_identifiers.remove(clean)

    def is_compliant(self, text: str) -> bool:
        """Checks if the text contains any blocked identifier."""
        if not self.blocked_identifiers or not text:
            return True

        text_lower = text.lower()
        for blocked in self.blocked_identifiers:
            if re.search(rf"\b{re.escape(blocked)}\b", text_lower):
                return False
        return True

    def postprocess_nodes(self, nodes: List[any], query_bundle: Optional[any] = None) -> List[any]:
        """
        Filters a list of NodeWithScore objects or generic node representations.
        """
        compliant_nodes = []
        for node_item in nodes:
            content = ""
            if hasattr(node_item, "node") and hasattr(node_item.node, "get_content"):
                content = node_item.node.get_content()
            elif hasattr(node_item, "get_content"):
                content = node_item.get_content()
            elif hasattr(node_item, "text"):
                content = node_item.text
            elif isinstance(node_item, dict):
                content = node_item.get("text", "")
            else:
                content = str(node_item)

            if self.is_compliant(content):
                compliant_nodes.append(node_item)

        return compliant_nodes