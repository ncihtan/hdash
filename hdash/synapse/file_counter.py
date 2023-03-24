"""File Counter."""
from hdash.synapse.meta_file import MetaFile
from pathlib import Path
import logging


class FileCounter:
    """File Counter."""

    BAM = "BAM"
    FASTQ = "FASTQ"
    IMAGE = "IMAGE"
    MATRIX = "MATRIX"
    METADATA = "METADATA"
    OTHER = "OTHER_ASSAY"
    EXCLUDE = "EXCLUDE"

    def __init__(self, synapse_df):
        """Construct new File Counter."""
        self._file_df = synapse_df[synapse_df.type == "file"]
        self._folder_df = synapse_df[synapse_df.type == "folder"]
        self._init_file_types()
        self._identify_archive_folders()
        self._walk_files()

    def get_num_files(self, file_type):
        """Get the File Type Counter."""
        return self.file_type_counter.get(file_type, 0)

    def get_total_file_size(self, file_type):
        """Get the Total File Size for the Specified File Type."""
        return self.file_size_counter.get(file_type, 0)

    def _identify_archive_folders(self):
        self.archive_folder_set = set()
        for index, row in self._folder_df.iterrows():
            name = row["name"]
            id = row["id"]
            if name.lower() == "archive":
                self.archive_folder_set.add(id)

    def _walk_files(self):
        file_type_list = []
        for index, row in self._file_df.iterrows():
            name = row["name"]
            parent_id = row["parentId"]
            path = Path(name)
            if parent_id in self.archive_folder_set:
                file_type = FileCounter.EXCLUDE
            elif name.startswith(".DS_Store"):
                file_type = FileCounter.EXCLUDE
            elif name == MetaFile.LEGACY_META_FILE_NAME:
                file_type = FileCounter.EXCLUDE
            elif name.startswith(MetaFile.META_FILE_PREFIX):
                file_type = FileCounter.METADATA
            else:
                if path.suffix == ".gz":
                    file_extension = "".join(path.suffixes[-2])
                else:
                    file_extension = path.suffix
                try:
                    file_type = self.file_type_map[file_extension]
                except KeyError:
                    logging.warning(
                        "Unrecognized File Extension: %s [%s]" % (file_extension, path)
                    )
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
        fm[".fasta"] = FileCounter.FASTQ
        fm[".fq"] = FileCounter.FASTQ
        fm[".tif"] = FileCounter.IMAGE
        fm[".tiff"] = FileCounter.IMAGE
        fm[".svs"] = FileCounter.IMAGE
        fm[".vsi"] = FileCounter.IMAGE
        fm[".png"] = FileCounter.IMAGE
        fm[".raw"] = FileCounter.IMAGE
        fm[".jpg"] = FileCounter.IMAGE
        fm[".scn"] = FileCounter.IMAGE
        fm[".s0001_e00"] = FileCounter.IMAGE
        fm[".csv"] = FileCounter.MATRIX
        fm[".tsv"] = FileCounter.MATRIX
        fm[".vcf"] = FileCounter.MATRIX
        fm[".fcs"] = FileCounter.MATRIX
        fm[".mtx"] = FileCounter.MATRIX
        fm[".txt"] = FileCounter.MATRIX
        fm[".h5ad"] = FileCounter.MATRIX
        fm[".h5"] = FileCounter.MATRIX
        fm[".xlsx"] = FileCounter.MATRIX
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
