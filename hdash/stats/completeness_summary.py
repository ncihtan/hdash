from hdash.synapse.meta_map import MetaMap
from hdash.graph.graph_flattener import GraphFlattener
from hdash.graph.key import KeyUtil
from hdash.util.id_util import IdUtil
from hdash.validator.categories import Categories


class CompletenessSummary:
    """
    Assesses how complete the data set is.

    For example:
    - given patient 1, do we have metadata for diagnosis, therapy, etc?
    - given biospecimen 1, do we have data for all levels of RNASeq?
    """

    def __init__(self, atlas_id, meta_map: MetaMap, graph_flat: GraphFlattener):
        """Default Constructor."""
        self.atlas_id = atlas_id
        self.meta_map = meta_map
        self.graph_flat = graph_flat
        self.completeness_map = set()
        self.id_util = IdUtil()
        self.categories = Categories()

        # Assess Clinical Categories
        for clinical_category in self.categories.all_clinical:
            self.__walk_clinical_category(clinical_category)

    def has_data(self, primary_id, category):
        """Determine if the specified ID has data of the specified category."""
        key = KeyUtil.create_key(primary_id, category)
        if category in self.categories.all_clinical:
            return key in self.completeness_map
        else:
            return self.graph_flat.biospecimen_has_assay(primary_id, category)

    def __walk_clinical_category(self, category):
        """Walk through specified clinical category."""
        meta_file_list = self.meta_map.get_meta_file_list(category)
        for meta_file in meta_file_list:
            self.__inspect_clinical_df(category, meta_file.df)

    def __inspect_clinical_df(self, category, df):
        """Inspect Data Frame for Primary IDs."""
        for index, row in df.iterrows():
            primary_id_column = self.id_util.get_primary_id_column(category)
            primary_id = row[primary_id_column]

            key = KeyUtil.create_key(primary_id, category)
            self.completeness_map.add(key)
