"""Test FileCounter class."""
import pandas as pd
from hdash.synapse.file_counter import FileCounter


def test_file_counter_1():
    """Round 1 of file counter tests."""
    file_names = ["hta1.bam", "hta1.fq", "hta.tif", "hta2.bam"]
    file_sizes = [100, 100, 100, 100]
    cols = ["name", "dataFileSizeBytes"]
    file_df = pd.DataFrame(list(zip(file_names, file_sizes)), columns=cols)
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
    cols = ["name", "dataFileSizeBytes"]
    file_df = pd.DataFrame(list(zip(file_names, file_sizes)), columns=cols)
    counter = FileCounter(file_df)
    assert counter.get_num_files(FileCounter.OTHER) == 1
    assert counter.get_total_file_size(FileCounter.OTHER) == 100
