"""Test FileCounter class."""
import pandas as pd
from hdash.synapse.file_counter import FileCounter


def test_file_counter_1():
    """Round 1 of file counter tests."""
    file_names = ["hta1.bam", "hta1.fq", "hta.tif", "hta2.bam"]
    file_sizes = [100, 100, 100, 100]
    file_types = ["file", "file", "file", "file"]
    ids = ["a1", "a2", "a3", "a4"]
    parent_ids = ["b1", "b2", "b3", "b4"]
    cols = ["id", "name", "type", "dataFileSizeBytes", "parentId"]
    zipped = list(zip(ids, file_names, file_types, file_sizes, parent_ids))
    file_df = pd.DataFrame(zipped, columns=cols)
    counter = FileCounter(file_df)
    assert counter.get_num_files(FileCounter.BAM) == 2
    assert counter.get_num_files(FileCounter.FASTQ) == 1
    assert counter.get_num_files(FileCounter.IMAGE) == 1
    assert counter.get_num_files(FileCounter.OTHER) == 0

    assert counter.get_total_file_size(FileCounter.BAM) == 200
    assert counter.get_total_file_size(FileCounter.FASTQ) == 100
    assert counter.get_total_file_size(FileCounter.IMAGE) == 100
    assert counter.get_total_file_size(FileCounter.OTHER) == 0


def test_file_counter_2():
    """Round 2 of file counter tests."""
    file_names = ["hta1.bam", "hta1.fq", "hta.tif", "hta2.uidd"]
    file_sizes = [100, 100, 100, 100]
    file_types = ["file", "file", "file", "file"]
    ids = ["a1", "a2", "a3", "a4"]
    parent_ids = ["b1", "b2", "b3", "b4"]
    cols = ["id", "name", "type", "dataFileSizeBytes", "parentId"]
    zipped = list(zip(ids, file_names, file_types, file_sizes, parent_ids))
    file_df = pd.DataFrame(zipped, columns=cols)
    counter = FileCounter(file_df)
    assert counter.get_num_files(FileCounter.OTHER) == 1
    assert counter.get_total_file_size(FileCounter.OTHER) == 100


def test_archive_files():
    """Verify that archive files are not counted."""
    file_names = ["hta1.bam", "hta1.fq", "hta.tif", "archive"]
    file_sizes = [100, 100, 100, 100]
    file_types = ["file", "file", "file", "folder"]
    ids = ["a1", "a2", "a3", "a4"]
    parent_ids = ["b1", "b1", "a4", "b1"]
    cols = ["id", "name", "type", "dataFileSizeBytes", "parentId"]
    zipped = list(zip(ids, file_names, file_types, file_sizes, parent_ids))
    file_df = pd.DataFrame(zipped, columns=cols)
    counter = FileCounter(file_df)
    assert counter.get_num_files(FileCounter.BAM) == 1
    assert counter.get_num_files(FileCounter.FASTQ) == 1
    assert counter.get_num_files(FileCounter.IMAGE) == 0
    assert counter.get_num_files(FileCounter.OTHER) == 0

    assert counter.get_total_file_size(FileCounter.BAM) == 100
    assert counter.get_total_file_size(FileCounter.FASTQ) == 100
    assert counter.get_total_file_size(FileCounter.IMAGE) == 0
    assert counter.get_total_file_size(FileCounter.OTHER) == 0
