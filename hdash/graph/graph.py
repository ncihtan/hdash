"""Graph Objects."""


class Node:
    """Node in Graph."""

    id: str
    sif_id: str
    label: str
    category: str

    def __repr__(self):
        """Get node summary."""
        return "Node: %s: %s: %s" % (self.id, self.label, self.category)


class Edge:
    """Edge in Graph."""

    source_id: str
    target_id: str

    def __repr__(self):
        """Get edge summary."""
        return "Edge: %s --> %s" % (self.source_id, self.target_id)
