"""Table Utilities."""
from hdash.synapse.htan_project import HTANProject
from hdash.synapse.meta_file import MetaFile
from hdash.synapse.file_counter import FileCounter
from hdash.synapse.synapse_util import SynapseUtil
import pandas as pd


class TableUtil:
    """Table Utilities."""

    def get_project_list(self, project_df):
        """Get the Project List from the specified project file."""
        project_list = []
        for row in project_df.itertuples():
            project = HTANProject()
            project.id = row.id
            project.atlas_id = row.atlas_id
            project.name = row.name
            project.liaison = row.liaison
            project.notes = row.notes
            project_list.append(project)
        return project_list

    def annotate_project_list(self, project_list, master_table_file):
        """Annotate the project list with file types and metadata info."""
        df = pd.read_csv(master_table_file)
        for project in project_list:
            self._count_files(df, project)
            self._extract_meta(df, project)

    def annotate_meta_file(self, meta_file: MetaFile):
        """Annotate the specified meta_file with additional details."""
        df = pd.read_csv(meta_file.path)
        component_list = df.Component.dropna().unique()
        try:
            meta_file.category = component_list[0]
        except IndexError:
            meta_file.category = "Empty"
        meta_file.df = df
        meta_file.num_items = len(df.index)

    def _count_files(self, df, project):
        target_df = df[(df.projectId == project.id)]
        counter = FileCounter(target_df)
        project.num_fastq = counter.get_num_files(FileCounter.FASTQ)
        project.num_bam = counter.get_num_files(FileCounter.BAM)
        project.num_image = counter.get_num_files(FileCounter.IMAGE)
        project.num_matrix = counter.get_num_files(FileCounter.MATRIX)
        project.num_other = counter.get_num_files(FileCounter.OTHER)
        project.num_meta = counter.get_num_files(FileCounter.METADATA)

        project.size_fastq = counter.get_total_file_size(FileCounter.FASTQ)
        project.size_bam = counter.get_total_file_size(FileCounter.BAM)
        project.size_image = counter.get_total_file_size(FileCounter.IMAGE)
        project.size_matrix = counter.get_total_file_size(FileCounter.MATRIX)
        project.size_other = counter.get_total_file_size(FileCounter.OTHER)

    def _extract_meta(self, df, project):
        target_df = df[
            (df.projectId == project.id)
            & (df.name.str.startswith(MetaFile.META_FILE_PREFIX))
        ]

        folder_map = {}
        for row in target_df.itertuples():
            meta_file = MetaFile()
            meta_file.id = row.id
            meta_file.modified_on = row.modifiedOn
            meta_file.parent_id = row.parentId
            meta_file.path = SynapseUtil.CACHE + "/" + row.id + ".csv"

            # A single folder may have two or more metadata files.
            # If this occurs, we only want the most recently modified metadata file.
            if meta_file.parent_id in folder_map:
                map_file = folder_map[meta_file.parent_id]
                if meta_file.modified_on > map_file.modified_on:
                    folder_map[meta_file.parent_id] = meta_file
            else:
                folder_map[meta_file.parent_id] = meta_file
        project.meta_list = list(folder_map.values())
