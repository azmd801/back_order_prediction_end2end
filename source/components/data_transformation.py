import sys

import numpy as np
import pandas as pd
from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler

from source.constants.training_pipeline import TARGET_COLUMN
from source.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact,
)
from source.entity.config_entity import DataTransformationConfig
from source.exception import BackOrderException
from source.logger import logging
# from sensor.ml.model.estimator import TargetValueMapping
from source.utils import save_numpy_array_data, save_object


class DataTransformation:
    def __init__(
        self,
        data_validation_artifact: DataValidationArtifact,
        data_transformation_config: DataTransformationConfig,
    ):
        """

        :param data_validation_artifact: Output reference of data ingestion artifact stage
        :param data_transformation_config: configuration for data transformation
        """
        try:
            self.data_validation_artifact = data_validation_artifact

            self.data_transformation_config = data_transformation_config

        except Exception as e:
            raise BackOrderException(e, sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)

        except Exception as e:
            raise BackOrderException(e, sys)

    @classmethod
    def get_data_transformer_object(cls) -> Pipeline:
        pass

    def initiate_data_transformation(self,) -> DataTransformationArtifact:
        pass