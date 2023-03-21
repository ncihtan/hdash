from typing import List
from hdash.synapse.meta_file import MetaFile


class MetaMap:
    """
    MetaMap Class.

    This class maps a category, e.g. "ImagingLevel1" to one or more MetaFiles.
    """

    def __init__(self):
        """Construct new MetaMap File."""
        self.map = {}

    def add_meta_file(self, meta_file:  MetaFile):
        """Add new Meta File to the Map."""
        category = meta_file.category
        if category in self.map:
            meta_list = self.map[category]
            meta_list.append(meta_file)
        else:
            self.map[category] = [meta_file]

    def has_category(self, category: str):
        """Determine if the MetaMap has data for the specified category."""
        return category in self.map

    def get_meta_file_list(self, category: str) -> List[MetaFile]:
        """Get the List of Meta Files Associated with the Specified Category."""
        return self.map.get(category, [])

    def get_categories(self) -> List[str]:
        """Get the list of all registered categories in the map."""
        return self.map.keys()
