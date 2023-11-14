import sys

import numpy as np
import pandas as pd
from pandas import DataFrame

from source.cloud_storage.aws_storage import SimpleStorageService
from source.constants.training_pipeline import SCHEMA_FILE_PATH
from source.entity.config_entity import PredictionPipelineConfig
from source.exception import BackOrderException
from source.logger import logging
from source.ml.s3_estimator import BackOrderEstimator
from source.utils import read_yaml_file
from source.ml.pre_processing import drop_columns


class PredictionPipeline:
    """
    PredictionPipeline is a class that handles the prediction pipeline for back order prediction.

    Attributes:
        prediction_pipeline_config (PredictionPipelineConfig):
            Configuration for the prediction pipeline.
        s3 (SimpleStorageService):
            An instance of SimpleStorageService for handling interactions with Amazon S3.


    Methods:
        get_data():
            Retrieve prediction data from an S3 bucket.

        get_model():
            Load the prediction model from an S3 bucket.

        predict(model, dataframe):
            Make predictions using the provided model and input data.

        get_labels(model, prediction_array):
            Get the original labels from the model.

        initiate_prediction():
            Initiate the prediction pipeline.

    """

    def __init__(
        self,
        prediction_pipeline_config: PredictionPipelineConfig = PredictionPipelineConfig(),
    ) -> None:
        """
        Initialize the PredictionPipeline.
        """

        try:

            self.prediction_pipeline_config = prediction_pipeline_config

            self.s3 = SimpleStorageService()

        except Exception as e:
            raise (BackOrderException, sys)

    def get_data(self) -> DataFrame:
        """
        Retrieve prediction data from an S3 bucket.
        """
        try:
            logging.info("Entered get_data method of PredictionPipeline class")

            prediction_df = self.s3.read_csv(
                filename=self.prediction_pipeline_config.data_file_path,
                bucket_name=self.prediction_pipeline_config.data_bucket_name,
            )

            logging.info("Read prediction csv file from s3 bucket")

            logging.info(f"prediction_df \n\n:{prediction_df}")

            # prediction_df = drop_columns(prediction_df)

            # logging.info("Dropped the required columns")

            logging.info("Exited the get_data method of PredictionPipeline class")

            return prediction_df

        except Exception as e:
            raise BackOrderException(e, sys)
        
    def get_model(self) -> object:
        """
        Load the prediction model from an S3 bucket.
        """

        try:
            logging.info("Entered predict method of PredictionPipeline class")

            back_order_estimator = BackOrderEstimator(
                bucket_name=self.prediction_pipeline_config.model_bucket_name,
                model_path=self.prediction_pipeline_config.model_file_path,
            )

            model = back_order_estimator.load_model()
            return model
            
        except Exception as e:
            raise BackOrderException(e, sys)            

    def predict(self,model, dataframe) -> np.ndarray:
        """
        Make predictions using the provided model and input data.
        """

        try:
            logging.info("Entered predict method of PredictionPipeline class")

            return model.predict(dataframe)

        except Exception as e:
            raise BackOrderException(e, sys)
        
    def get_labels(self,model,prediction_array) -> np.ndarray:
        """
        Get the original labels from the model.
        """

        try:
            logging.info("Entered get_labels method of PredictionPipeline class")

            return model.get_original_labels(prediction_array)

        except Exception as e:
            raise BackOrderException(e, sys)


    def initiate_prediction(self,) -> None:
        """
        Initiate the prediction pipeline.
        """
        
        try:
            logging.info("Starting prediction pipeline")

            dataframe = self.get_data()
            
            model = self.get_model()

            predicted_arr = self.predict(model,dataframe)

            predicted_labels = self.get_labels(model,predicted_arr)

            prediction = pd.DataFrame(list(predicted_labels))

            prediction.columns = ["class"]

            predicted_dataframe = pd.concat([dataframe, prediction], axis=1)

            self.s3.upload_df_as_csv(
                predicted_dataframe,
                self.prediction_pipeline_config.output_file_name,
                self.prediction_pipeline_config.output_file_name,
                self.prediction_pipeline_config.data_bucket_name,
            )

            logging.info("Uploaded artifacts folder to s3 bucket_name")

            logging.info(f"File has uploaded to\n\n {predicted_dataframe}")

            logging.info(f"Exiting prediction pipeline")

        except Exception as e:
            raise BackOrderException(e, sys)
