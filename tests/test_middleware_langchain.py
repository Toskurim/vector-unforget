"""
Test Suite: LangChain Middleware Integration for VectorUnforget.
Author: Toskurim
"""

from vector_unforget.middleware.langchain_retriever import VectorUnforgetRetriever


class MockDocument:
    def __init__(self, page_content: str, metadata: dict = None):
        self.page_content = page_content
        self.metadata = metadata or {}


class MockLangChainRetriever:
    def invoke(self, query: str):
        return [
            MockDocument("Alice Rossi profile, SSN: 123-45-6789, email: alice@example.com"),
            MockDocument("Bob Smith report on mechanical parts and CNC operations."),
            MockDocument("Anonymous transaction log from IP 192.168.1.100 containing telemetry."),
            MockDocument("Charlie Brown general notes without any sensitive record."),
        ]


def test_vector_unforget_retriever_filters_blocked_pii():
    mock_base = MockLangChainRetriever()
    retriever = VectorUnforgetRetriever(
        base_retriever=mock_base,
        blocked_identifiers={"alice rossi", "192.168.1.100"},
    )

    results = retriever.invoke("get all records")

    # Only Bob and Charlie should remain
    assert len(results) == 2
    contents = [d.page_content for d in results]
    assert any("Bob Smith" in c for c in contents)
    assert any("Charlie Brown" in c for c in contents)
    assert not any("Alice Rossi" in c for c in contents)
    assert not any("192.168.1.100" in c for c in contents)


def test_dynamic_blocking():
    mock_base = MockLangChainRetriever()
    retriever = VectorUnforgetRetriever(base_retriever=mock_base)

    # Initial query returns all 4
    all_results = retriever.invoke("all")
    assert len(all_results) == 4

    # Dynamically block Bob
    retriever.add_blocked_identifier("Bob Smith")
    filtered_results = retriever.invoke("all")
    assert len(filtered_results) == 3


if __name__ == "__main__":
    test_vector_unforget_retriever_filters_blocked_pii()
    test_dynamic_blocking()
    print("✅ LangChain Middleware tests passed successfully!")