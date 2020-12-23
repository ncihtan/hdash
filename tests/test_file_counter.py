"""Test FileCounter class."""

from hdash.synapse.file_counter import FileCounter
from click import File


def test_file_counter():
  file_list = ["hta1.bam", "hta1.fq", "hta.tif", "hta2.bam"]
  counter = FileCounter(file_list)
  assert counter.get_num_files(FileCounter.BAM) == 2
  assert counter.get_num_files(FileCounter.FASTQ) == 1
  assert counter.get_num_files(FileCounter.IMAGE) == 1
