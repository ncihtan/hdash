"""File Counter."""
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
    EXCLUDE = "EXCLUDE"

    def __init__(self, file_df):
        """Construct new File Counter."""
        self._file_df = file_df
        self._init_file_types()
        self._walk_files()

    def get_num_files(self, file_type):
        """Get the File Type Counter."""
        return self.file_type_counter.get(file_type, 0)

    def get_total_file_size(self, file_type):
        """Get the Total File Size for the Specified File Type."""
        return self.file_size_counter.get(file_type, 0)

    def _walk_files(self):
        file_type_list = []
        for index, row in self._file_df.iterrows():
            name = row["name"]
            path = Path(name)
            if name == MetaFile.META_FILE_NAME:
                file_type = FileCounter.METADATA
            else:
                if path.suffix == ".gz":
                    file_extension = "".join(path.suffixes[0:2])
                else:
                    file_extension = path.suffix
                try:
                    file_type = self.file_type_map[file_extension]
                except KeyError:
                    logging.warning("Unrecognized: %s" % file_extension)
                    file_type = FileCounter.OTHER
            file_type_list.append(file_type)

        # Aggregate counts by file type
        self._file_df.insert(0, "file_type", file_type_list)
        groups = self._file_df.groupby("file_type")["file_type"].count()
        self.file_type_counter = groups.to_dict()
        groups = self._file_df.groupby("file_type")["dataFileSizeBytes"].sum()
        self.file_size_counter = groups.to_dict()

    def _init_file_types(self):
        fm = {}
        fm[".bam"] = FileCounter.BAM
        fm[".fastq"] = FileCounter.FASTQ
        fm[".fastq.gz"] = FileCounter.FASTQ
        fm[".fq.gz"] = FileCounter.FASTQ
        fm[".fq"] = FileCounter.FASTQ
        fm[".tif"] = FileCounter.IMAGE
        fm[".tiff"] = FileCounter.IMAGE
        fm[".svs"] = FileCounter.IMAGE
        fm[".vsi"] = FileCounter.IMAGE
        fm[".png"] = FileCounter.IMAGE
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

        fm[".DS_Store"] = FileCounter.EXCLUDE
        fm[".vimrc"] = FileCounter.EXCLUDE
        fm[".Rhistory"] = FileCounter.EXCLUDE
        self.file_type_map = fm
