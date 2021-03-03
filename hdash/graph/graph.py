"""Graph Objects."""


class Node:
    """Node in Graph."""

    id: str
    label: str
    category: str

    def __repr__(self):
        """Get node summary."""
        return "Node: %s: %s: %s" % (self.id, self.label, self.category)


class Edge:
    """Edge in Graph."""

    source: str
    target: str
    category: str

    def __repr__(self):
        """Get edge summary."""
        return "Edge: %s: %s: %s" % (self.source, self.target, self.category)
