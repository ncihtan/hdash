import pandas as pd
from hdash.validator.validation_h1 import ValidationH1
from hdash.validator.validation_h2 import ValidationH2


class HtanValidator:
    def __init__(self, atlas_id, meta_data_file_list):

        self.atlas_id = atlas_id
        self.validation_list = []

        # First step is to read in all the metadata files and caterogize them
        self.meta_map = {}
        for path in meta_data_file_list:
            current_df = pd.read_csv(path)
            component_list = current_df["Component"].to_list()
            component = component_list[0]
            self.meta_map[component] = current_df
        self.__validate()

    def get_validation_list(self):
        return self.validation_list

    def __validate(self):
        h1 = ValidationH1(self.meta_map)
        self.validation_list.append(h1)

        if h1.validation_passed:
            h2 = ValidationH2(self.atlas_id, self.meta_map)
            self.validation_list.append(h2)
