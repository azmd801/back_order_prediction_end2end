import json
import sys

import pandas as pd
# from evidently.model_profile import Profile
# from evidently.model_profile.sections import DataDriftProfileSection
from pandas import DataFrame

from source.constants.training_pipeline import SCHEMA_FILE_PATH
from source.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from source.entity.config_entity import DataValidationConfig
from source.exception import BackOrderException
from source.logger import logging
from source.utils import read_yaml_file, write_yaml_file


class DataValidation:
    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_config: DataValidationConfig,
    ):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
            
        except Exception as e:
            raise BackOrderException(e, sys)

    @ staticmethod
    def read_data(file_path) -> pd.DataFrame:
        pass

    def validate_number_of_columns(self) -> bool:
        pass

    def is_numerical_columns_exist(self) -> bool:
        pass

    def is_categorical_column_exist(self) -> bool:
        pass

    def detect_dataset_drift(self):
        pass

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            pass

        except Exception as e:
            raise BackOrderException(e, sys) from e  

