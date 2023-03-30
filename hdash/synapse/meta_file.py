class MetaFile:
    """Metadata File."""

    LEGACY_META_FILE_NAME = "synapse_storage_manifest.csv"
    META_FILE_PREFIX = "synapse_storage_manifest_"

    def __init__(self):
        """Construct new Metadata File."""
        self.id = None
        self.path = None
        self.category = None
        self.num_items = 0
        self.parent_id = None
        self.modified_on = None
        self.df = None
        self.percent_meta_data_complete = 0

    def __repr__(self):
        """Return summary of object."""
        return "%s: %s [%d items]" % (self.id, self.category, self.num_items)
