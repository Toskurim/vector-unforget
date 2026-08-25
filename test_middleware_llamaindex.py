"""
Test Suite: LlamaIndex Node Postprocessor Integration.
Author: Toskurim
"""

from vector_unforget.middleware.llamaindex_processor import VectorUnforgetNodePostprocessor


class MockNode:
    def __init__(self, text: str):
        self.text = text

    def get_content(self) -> str:
        return self.text


class MockNodeWithScore:
    def __init__(self, text: str, score: float = 0.95):
        self.node = MockNode(text)
        self.score = score


def test_llamaindex_postprocessor_filters_nodes():
    nodes = [
        MockNodeWithScore("Customer record for Mario Rossi, CF: RSSMRA85M01H501Z, balance: 1200EUR"),
        MockNodeWithScore("Technical architecture overview for internal API microservices."),
        MockNodeWithScore("Orphaned log entry with IP 10.0.0.45 linked to deleted session."),
    ]

    postprocessor = VectorUnforgetNodePostprocessor(
        blocked_identifiers={"mario rossi", "10.0.0.45"}
    )

    filtered_nodes = postprocessor.postprocess_nodes(nodes)

    assert len(filtered_nodes) == 1
    assert "Technical architecture" in filtered_nodes[0].node.get_content()
    assert not any("Mario Rossi" in n.node.get_content() for n in filtered_nodes)
    assert not any("10.0.0.45" in n.node.get_content() for n in filtered_nodes)


def test_dynamic_update():
    nodes = [
        MockNodeWithScore("Confidential design specs for component X."),
        MockNodeWithScore("Employee record: John Doe, SSN: 000-11-2222."),
    ]

    postprocessor = VectorUnforgetNodePostprocessor()
    assert len(postprocessor.postprocess_nodes(nodes)) == 2

    postprocessor.add_blocked_identifier("000-11-2222")
    filtered = postprocessor.postprocess_nodes(nodes)
    assert len(filtered) == 1
    assert "Confidential design specs" in filtered[0].node.get_content()


if __name__ == "__main__":
    test_llamaindex_postprocessor_filters_nodes()
    test_dynamic_update()
    print("✅ LlamaIndex Middleware tests passed successfully!")