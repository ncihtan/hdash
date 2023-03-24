"""HTAN Project."""
import humanize


class HTANProject:
    """HTAN Project."""

    def __init__(self):
        """Construct new HTAN Project."""
        self.id = None
        self.atlas_id = None
        self.name = None
        self.liaison = None
        self.notes = None
        self.num_fastq = 0
        self.num_bam = 0
        self.num_image = 0
        self.num_matrix = 0
        self.num_other = 0
        self.num_meta = 0
        self.size_fastq = 0
        self.size_bam = 0
        self.size_image = 0
        self.size_matrix = 0
        self.size_other = 0
        self.meta_list = []
        self.validation_list = []
        self.num_errors = 0
        self.percent_meta_data_complete = 0
        self.meta_map = None
        self.htan_graph = None
        self.flat_graph = None
        self.sif = None
        self.completeness_stats = None
        self.heatmap_list = []

    def get_total_num_files(self):
        """Get total number of files."""
        return self.num_fastq + self.num_bam + self.num_image + self.num_matrix + self.num_other

    def get_total_file_size(self):
        """Get total file size."""
        return (
            self.size_fastq
            + self.size_bam
            + self.size_image
            + self.size_matrix
            + self.size_other
        )

    def get_total_fize_size_human_readable(self):
        """Get total file size in human readable format, e.g. MB, TB."""
        total_file_size = self.get_total_file_size()
        return humanize.naturalsize(total_file_size)

    def __repr__(self):
        """Return summary of object."""
        return "%s: %s" % (self.id, self.name)
