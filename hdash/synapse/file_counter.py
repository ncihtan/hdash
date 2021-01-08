"""File Counter."""
from collections import Counter
from hdash.synapse.htan_project import MetaFile
from pathlib import Path
import logging


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

    def get_num_files(self, file_type):
        """Get the File Type Counter."""
        return self.counter[file_type]

    def _walk_files(self):
        for file in self.file_list:
            path = Path(file)
            if file == MetaFile.META_FILE_NAME:
                self.file_type_list.append(FileCounter.METADATA)
            elif file not in self.exclude_file_list:
                if path.suffix == ".gz":
                    file_extension = "".join(path.suffixes[0:2])
                else:
                    file_extension = path.suffix
                try:
                    file_type = self.file_type_map[file_extension]
                except KeyError:
                    logging.warning("Unrecognized: %s" % file_extension)
                    file_type = FileCounter.OTHER
                finally:
                    self.file_extension_list.append(file_extension)
                    self.file_type_list.append(file_type)
        self.counter = Counter(self.file_type_list)

    def _init_file_types(self):
        fm = {}
        fm[".bam"] = FileCounter.BAM
        fm[".fastq"] = FileCounter.FASTQ
        fm[".fastq.gz"] = FileCounter.FASTQ
        fm[".fq.gz"] = FileCounter.FASTQ
        fm[".fq"] = FileCounter.FASTQ
        fm[".tif"] = FileCounter.IMAGE
        fm[".csv"] = FileCounter.MATRIX
        fm[".csv.gz"] = FileCounter.MATRIX
        fm[".tsv"] = FileCounter.MATRIX
        fm[".tsv.gz"] = FileCounter.MATRIX
        fm[".mtx"] = FileCounter.MATRIX
        fm[".txt"] = FileCounter.MATRIX
        fm[".h5ad"] = FileCounter.MATRIX
        fm[".pdf"] = FileCounter.OTHER
        fm[".rnk"] = FileCounter.OTHER
        fm[".json"] = FileCounter.OTHER
        fm[".bcf"] = FileCounter.OTHER
        fm[".bzcfg"] = FileCounter.OTHER
        fm[".log"] = FileCounter.OTHER
        fm[".mzML"] = FileCounter.OTHER
        fm[".zstd"] = FileCounter.OTHER
        self.file_type_map = fm

    def _init_exclude_list(self):
        el = []
        el.append(".DS_Store")
        el.append(".vimrc")
        el.append(".Rhistory")
        self.exclude_file_list = el
