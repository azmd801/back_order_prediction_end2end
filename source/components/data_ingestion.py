import os
import sys

from pandas import DataFrame
from sklearn.model_selection import train_test_split

from source.constants.training_pipeline import SCHEMA_DROP_COLS, SCHEMA_FILE_PATH
# from source.data_access.sensor_data import SensorData
from source.entity.artifact_entity import DataIngestionArtifact
from source.entity.config_entity import DataIngestionConfig
from source.exception import BackOrderException
from source.logger import logging
# from source.utils.main_utils import read_yaml_file


class DataIngestion:
    def __init__(
        self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()
    ):
        """

        """
        try:
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise BackOrderException(e, sys)

    def export_data_into_feature_store(self) -> DataFrame:
        try:
            pass
        except Exception as e:
            raise BackOrderException(e, sys) from e  
        
    def split_data_as_train_test(self, dataframe: DataFrame) -> None:
        try:
            pass
        except Exception as e:
            raise BackOrderException(e, sys) from e  

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            pass
        except Exception as e:
            raise BackOrderException(e, sys) from e  

        
