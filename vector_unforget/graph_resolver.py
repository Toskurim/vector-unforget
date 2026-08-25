"""
Graph-Based Cascading Entity Resolver for VectorUnforget.
Author: Toskurim
License: AGPLv3
"""

from typing import Dict, Set, List, Tuple, Any
from collections import defaultdict, deque


class PIIEntityGraph:
    """
    Constructs an in-memory bipartite/multi-relational graph linking chunks and PII.
    Enables multi-hop cascading erasure across arbitrary depth levels.
    """

    def __init__(self, decay_factor: float = 0.85):
        """
        :param decay_factor: Confidence reduction per graph hop/level (0.0 to 1.0).
        """
        self.decay_factor = decay_factor
        self.adjacency: Dict[str, Set[str]] = defaultdict(set)
        self.chunk_entities: Dict[str, Set[str]] = defaultdict(set)
        self.entity_chunks: Dict[str, Set[str]] = defaultdict(set)

    def add_relation(self, entity_a: str, entity_b: str) -> None:
        """Adds a bidirectional edge between two detected PII entities."""
        a, b = entity_a.strip().lower(), entity_b.strip().lower()
        if a and b and a != b:
            self.adjacency[a].add(b)
            self.adjacency[b].add(a)

    def link_chunk(self, chunk_id: str, entities: Set[str]) -> None:
        """Associates a chunk ID with all extracted entities in its text."""
        clean_entities = {e.strip().lower() for e in entities if e.strip()}
        self.chunk_entities[chunk_id].update(clean_entities)
        for e in clean_entities:
            self.entity_chunks[e].add(chunk_id)

        # Interlink all co-occurring entities in this chunk
        entity_list = list(clean_entities)
        for i in range(len(entity_list)):
            for j in range(i + 1, len(entity_list)):
                self.add_relation(entity_list[i], entity_list[j])

    def resolve_cascading_entities(
        self,
        seed_entity: str,
        max_depth: int = 3,
        min_confidence: float = 0.5,
    ) -> Dict[str, float]:
        """
        Traverses the entity graph starting from a seed entity up to max_depth.
        Returns a dictionary of connected entities and their confidence scores.
        """
        seed = seed_entity.strip().lower()
        confidence_map: Dict[str, float] = {seed: 1.0}
        queue = deque([(seed, 1.0, 0)])
        visited = {seed}

        while queue:
            current_entity, current_conf, depth = queue.popleft()
            if depth >= max_depth:
                continue

            for neighbor in self.adjacency.get(current_entity, []):
                new_conf = current_conf * self.decay_factor
                if neighbor not in visited and new_conf >= min_confidence:
                    visited.add(neighbor)
                    confidence_map[neighbor] = round(new_conf, 3)
                    queue.append((neighbor, new_conf, depth + 1))

        return confidence_map

    def get_affected_chunks(
        self,
        resolved_entities: Dict[str, float],
    ) -> Set[str]:
        """Returns all chunk IDs associated with the resolved entity set."""
        affected_chunks = set()
        for entity in resolved_entities:
            affected_chunks.update(self.entity_chunks.get(entity, set()))
        return affected_chunks