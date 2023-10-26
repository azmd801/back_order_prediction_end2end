import sys

import numpy as np
import pandas as pd
from imblearn.combine import SMOTETomek
from source.ml.pre_processing import Winsorizer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
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
from source.utils import read_yaml_file
from source.constants.training_pipeline import SCHEMA_DROP_COLS, SCHEMA_FILE_PATH
from sklearn.preprocessing import StandardScaler,OneHotEncoder,LabelEncoder


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
            
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)

        except Exception as e:
            raise BackOrderException(e, sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)

        except Exception as e:
            raise BackOrderException(e, sys)
        
    def drop_columns(self, df: pd.DataFrame) -> pd.DataFrame:
            """
            will drop unneccesary columns before data transformation
            """
            # _schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)

            # logging.info("Dropping not so usefull features")   

            df = df.drop(self._schema_config[SCHEMA_DROP_COLS], axis=1)

            logging.info(f"Features droped out:{self._schema_config[SCHEMA_DROP_COLS]}")

            return df


    def get_data_transformer_object(self) -> Pipeline:
        """
        :return: Pipeline object to transform dataset
        """
        logging.info(
            "Entered get_data_transformer_object method of DataTransformation class"
        )

        try:
            logging.info("Got numerical cols from schema config")

            numerical_cols = list(
                set(self._schema_config["numerical"]) - set(self._schema_config[SCHEMA_DROP_COLS])
                )

            logging.info(f"Numerical cols: {numerical_cols}")

            logging.info("Got categorical cols from schema config")

            categorical_cols = list(
                set(self._schema_config["categorical"]) - set(self._schema_config[SCHEMA_DROP_COLS]) -{TARGET_COLUMN}
                )
            
            logging.info(f"Categorical cols: {categorical_cols}")

            # components of numerical pipeline
            numerical_imputer = SimpleImputer(strategy="median", add_indicator=False)
            standard_scaler = StandardScaler()

            # logging.info(f"initialized standard scaler, simple imputer with median to transform numerical columns")

            # Constructing the numerical pipeline
            num_pipeline = Pipeline([
                ('scaler', standard_scaler),
                ('imputer', numerical_imputer),
                ('outlier_clipping', Winsorizer()),
            ])

            logging.info("pipeline to transform numerical columns is complete")

            # components of caegorical pipeline
            categorical_imputer = SimpleImputer(strategy="most_frequent", add_indicator=False)
            categorical_encoder = OneHotEncoder(drop='first')

            # logging.info(f"initialized categorical_imputer with most frequent strategey , simple imputer with median to transform numerical columns")

            # construting categorical pipeline
            cat_pipeline = Pipeline([
                ('imputer', categorical_imputer),
                ('encoder', categorical_encoder),
            ])

            logging.info("pipeline to transform categorical columns is complete")

            # combining numerical and categorical pipelines
            input_preprocessor = ColumnTransformer(
                transformers=[
                    ('num', num_pipeline, numerical_cols),
                    ('cat', cat_pipeline, categorical_cols),
                ]
            )
           
            logging.info(
                "created preprocessor object by combining numerical and categorical pipelines using ColumnTransformer"
                )

            logging.info(
                "Exited get_data_transformer_object method of DataTransformation class"
            )
            

            return input_preprocessor

        except Exception as e:
            raise BackOrderException(e, sys) from e


    def initiate_data_transformation(self,) -> DataTransformationArtifact:
        try:
            logging.info("Starting data transformation")

            preprocessor = self.get_data_transformer_object()

            logging.info("Got the preprocessor object")

            # getting train and test data set
            train_df = DataTransformation.read_data(
                self.data_validation_artifact.valid_train_file_path
            )[:1000]#for testing purpos only

            test_df = DataTransformation.read_data(
                file_path=self.data_validation_artifact.valid_test_file_path
            )[:1000]#for testing purpose only

            # dropping unnecessary features
            logging.info("dropping unnecessary features from train data set")

            train_df = self.drop_columns(train_df)

            logging.info("dropping unnecessary features from test data set")
            
            test_df = self.drop_columns(test_df)

            # getting train and target features
            # logging.info(f"trainging feature from train data set:{train_df.columns}")

            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)

            target_feature_train_df = train_df[TARGET_COLUMN]


            logging.info("Got train features and target features of Training dataset")

            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)

            target_feature_test_df = test_df[TARGET_COLUMN]

            logging.info("Got train features and target features of Testing dataset")

            # Transforming the training features 
            logging.info(
                "Applying preprocessing object on training dataframe and testing dataframe"
            )

            input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)

            logging.info(
                "Used the preprocessor object to fit transform the train features"
            )

            input_feature_test_arr = preprocessor.transform(input_feature_test_df)

            logging.info("Used the preprocessor object to transform the test features")

            # transforming the taget feature
            logging.info("Using the LabelEncoder to transform  input and test target feature")
            logging.info("Initializing the LabelEncoder")

            label_encoder = LabelEncoder()

            target_feature_train_arr = label_encoder.fit_transform(target_feature_train_df)

            logging.info("Applied LabelEncoder on training feature")

            target_feature_test_arr = label_encoder.transform(target_feature_test_df)

            logging.info("Applied LabelEncoder on test feature")

            # handling data imbalance
            logging.info("Applying SMOTETomek on Training dataset")

            smt = SMOTETomek(sampling_strategy="minority")

            input_feature_train_arr, target_feature_train_arr = smt.fit_resample(
                input_feature_train_arr, target_feature_train_arr
            )

            logging.info("Applied SMOTETomek on training dataset")

            train_arr = np.c_[
                input_feature_train_arr, target_feature_train_arr
            ]

            test_arr = np.c_[
                input_feature_test_arr, target_feature_test_arr
            ]

            save_object(
                self.data_transformation_config.preprocessor_object_file_path,
                preprocessor,
            )

            save_object(
                self.data_transformation_config.label_encoder_object_file_path,
                label_encoder,
            )            

            save_numpy_array_data(
                self.data_transformation_config.transformed_train_file_path,
                array=train_arr,
            )

            save_numpy_array_data(
                self.data_transformation_config.transformed_test_file_path,
                array=test_arr,
            )

            logging.info("Saved the preprocessor and label_encoder object")

            logging.info(
                "Exited initiate_data_transformation method of Data_Transformation class"
            )

            data_transformation_artifact = DataTransformationArtifact(
                preprocessor_object_file_path=self.data_transformation_config.preprocessor_object_file_path,
                label_encoder_object_file_path=self.data_transformation_config.label_encoder_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            )

            return data_transformation_artifact

        except Exception as e:
            raise BackOrderException(e, sys) from e