"""Test FileCounter class."""
from hdash.synapse.file_counter import FileCounter


def test_file_counter_1():
    file_list = ["hta1.bam", "hta1.fq", "hta.tif", "hta2.bam"]
    counter = FileCounter(file_list)
    assert counter.get_num_files(FileCounter.BAM) == 2
    assert counter.get_num_files(FileCounter.FASTQ) == 1
    assert counter.get_num_files(FileCounter.IMAGE) == 1
    assert counter.get_num_files(FileCounter.OTHER) == 0


def test_file_counter_2():
    file_list = ["hta1.bam", "hta1.fq", "hta.tif", "hta2.uidd"]
    counter = FileCounter(file_list)
    assert counter.get_num_files(FileCounter.OTHER) == 1
