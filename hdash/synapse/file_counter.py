"""File Counter."""
from collections import Counter
from pathlib import Path


class FileCounter:
    """File Counter."""

    BAM = "BAM"
    FASTQ = "FASTQ"
    IMAGE = "IMAGE"
    MATRIX = "MATRIX"
    METADATA = "METADATA"
    OTHER = "OTHER"

    def __init__(self, file_list):
        """Construct new File Counter."""
        self._init_file_types()
        self._init_exclude_list()
        self.file_list = file_list
        self.file_extension_list = []
        self.file_type_list = []
        self._walk_files()

    def _walk_files(self):

        # TODO:  Count the metada files
        for file in self.file_list:
            path = Path(file)
            if file == "synapse_storage_manifest.csv":
                self.file_type_list.append(FileCounter.METADATA)
            elif file not in self.exclude_file_list:
                if path.suffix == ".gz":
                    file_extension = "".join(path.suffixes[0:2])
                else:
                    file_extension = path.suffix
                file_type = self.file_type_map[file_extension]
                self.file_extension_list.append(file_extension)
                self.file_type_list.append(file_type)
        self.counter = Counter(self.file_type_list)

    def _init_file_types(self):
        fm = {}
        fm[".bam"] = FileCounter.BAM
        fm[".fastq"] = FileCounter.FASTQ
        fm[".fastq.gz"] = FileCounter.FASTQ
        fm[".tif"] = FileCounter.IMAGE
        fm[".csv"] = FileCounter.MATRIX
        fm[".mtx"] = FileCounter.MATRIX
        fm[".txt"] = FileCounter.MATRIX
        fm[".h5ad"] = FileCounter.MATRIX
        fm[".pdf"] = FileCounter.OTHER
        fm[".rnk"] = FileCounter.OTHER
        fm[".json"] = FileCounter.OTHER
        fm[".bcf"] = FileCounter.OTHER
        fm[".bzcfg"] = FileCounter.OTHER
        fm[".log"] = FileCounter.OTHER
        self.file_type_map = fm

    def _init_exclude_list(self):
        el = []
        el.append(".DS_Store")
        self.exclude_file_list = el

    def get_file_type_counter(self):
        """Get the File Type Counter."""
        return self.counter
