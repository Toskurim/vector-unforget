"""
Test Suite: Graph-Based Cascading Erasure.
Author: Toskurim
"""

from vector_unforget.graph_resolver import PIIEntityGraph


def test_graph_multi_hop_resolution():
    graph = PIIEntityGraph(decay_factor=0.8)

    # Chunk 1: Primary user with email
    graph.link_chunk("chunk_1", {"Mario Rossi", "mario.rossi@email.com"})

    # Chunk 2: Email associated with an IP address (Hop 1)
    graph.link_chunk("chunk_2", {"mario.rossi@email.com", "192.168.1.50"})

    # Chunk 3: IP address associated with an IBAN (Hop 2)
    graph.link_chunk("chunk_3", {"192.168.1.50", "IT60X0542811101000000123456"})

    # Chunk 4: Unrelated user data
    graph.link_chunk("chunk_4", {"Luigi Bianchi", "luigi@email.com"})

    # Resolve cascade from Mario Rossi (Depth 3)
    resolved = graph.resolve_cascading_entities("Mario Rossi", max_depth=3, min_confidence=0.5)

    assert "mario rossi" in resolved
    assert "mario.rossi@email.com" in resolved
    assert "192.168.1.50" in resolved
    assert "it60x0542811101000000123456" in resolved
    assert "luigi bianchi" not in resolved

    # Verify decay
    assert resolved["mario rossi"] == 1.0
    assert resolved["mario.rossi@email.com"] == 0.8
    assert resolved["192.168.1.50"] == 0.64
    assert resolved["it60x0542811101000000123456"] == 0.512

    # Check affected chunks
    chunks = graph.get_affected_chunks(resolved)
    assert chunks == {"chunk_1", "chunk_2", "chunk_3"}
    assert "chunk_4" not in chunks


if __name__ == "__main__":
    test_graph_multi_hop_resolution()
    print("✅ Graph-Based Cascading Erasure tests passed successfully!")