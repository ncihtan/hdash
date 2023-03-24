"""Node Data."""
from hdash.synapse.meta_file import MetaFile
from hdash.validator.categories import Categories


class NodeData:
    """Node Data."""

    id: str
    sif_id: str
    meta_file: MetaFile

    def __init__(self, id: str, meta_file: MetaFile):
        """Default Constructor"""
        self.id = id
        self.meta_file = meta_file
        self.abbrev_map = Categories().abbrev_category_map

    @property
    def sif_id(self):
        return self.abbrev_map[self.meta_file.category] + "_" + self.id

    def __repr__(self):
        """Get node summary."""
        return "Node: %s: %s" % (self.id, self.meta_file.category)
