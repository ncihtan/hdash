import pandas as pd
from hdash.validator.validation_h1 import ValidationH1


class HtanValidator:
    def __init__(self, htan_atlas_id, meta_data_file_list):

        self.__validation_list = []

        # First step is to read in all the metadata files and caterogize them
        self.__meta_map = {}
        for path in meta_data_file_list:
            current_df = pd.read_csv(path)
            component_list = current_df["Component"].to_list()
            component = component_list[0]
            self.__meta_map[component] = current_df
        self.__validate()

    def get_validation_list(self):
        return self.__validation_list

    def __validate(self):
        self.__validation_list.append(ValidationH1(self.__meta_map))
