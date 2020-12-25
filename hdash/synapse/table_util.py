"""Table Utilities."""
from hdash.synapse.htan_project import HTANProject
from hdash.synapse.file_counter import FileCounter
import pandas as pd


class TableUtil:
    """Table Utilities."""

    def annotate_project_list(self, project_list, master_table_file):
        """Annotate the project list with file types."""
        df = pd.read_csv(master_table_file)
        for project in project_list:
            target_df = df[(df.projectId == project.id) & (df.type == "file")]
            file_list = target_df.name.to_list()
            counter = FileCounter(file_list)
            project.num_fastq = counter.get_num_files(FileCounter.FASTQ)
            project.num_bam = counter.get_num_files(FileCounter.BAM)
            project.num_image = counter.get_num_files(FileCounter.IMAGE)
            project.num_matrix = counter.get_num_files(FileCounter.MATRIX)
            project.num_other = counter.get_num_files(FileCounter.OTHER)
            project.num_meta = counter.get_num_files(FileCounter.METADATA)

    def get_project_list(self, project_file):
        """Get the Project List from the specified project file."""
        df = pd.read_csv(project_file)
        project_list = []
        for row in df.itertuples():
            project = HTANProject()
            project.id = row.id
            project.name = row.name
            project.liaison = row.liaison
            project.notes = row.notes
            project_list.append(project)
        return project_list
