"""HTAN Project."""


class HTANProject:
    """HTAN Project."""

    def __init__(self):
        """Construct new HTAN Project."""
        self.id = None
        self.name = None
        self.liaison = None
        self.notes = None
        self.num_fastq = 0
        self.num_bam = 0
        self.num_image = 0
        self.num_matrix = 0
        self.num_other = 0
        self.num_meta = 0
        self.meta_list = []

    def __repr__(self):
        """Return summary of object."""
        return "%s: %s" % (self.id, self.name)


class MetaFile:
    """Metadata File."""

    META_FILE_NAME = "synapse_storage_manifest.csv"

    def __init__(self):
        """Construct new Metadata File."""
        self.id = None
        self.category = None
        self.num_items = 0

    def __repr__(self):
        """Return summary of object."""
        return "%s: %s [%d items]" % (self.id, self.category, self.num_items)
