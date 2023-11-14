import sys
import os
from pandas import DataFrame
from sklearn.pipeline import Pipeline
from source.constants.training_pipeline import MODEL_FILE_NAME,SAVED_MODEL_DIR
from source.exception import BackOrderException
from source.logger import logging
import numpy as np


class BackOrderPredictionModel:
    """
    This class encapsulates the essential components required for predicting back-order status:

    Args:
        preprocessing_object (Pipeline): A data preprocessing pipeline.
        trained_model_object (object): A trained prediction model.
        label_encoder_object (object): An object for label encoding.

    Methods:
        predict(dataframe: DataFrame) -> DataFrame:
            Utilizes the trained model to predict back-order status for a given DataFrame.

        get_original_labels(prediction_array: np.array) -> np.array:
            Converts predicted label indices back to their original labels using the label encoder.

        __repr__() -> str:
            Provides a string representation of the class.

        __str__() -> str:
            Offers a human-readable string representation of the class.
    """

    def __init__(
            self, preprocessing_object: Pipeline, 
            trained_model_object: object,
            label_encoder_object: object
            ):
        """
        Initialize the BackOrderPredictionModel instance.
        """

        self.preprocessing_object = preprocessing_object

        self.trained_model_object = trained_model_object

        self.label_encoder_object = label_encoder_object

    def predict(self, dataframe: DataFrame) -> DataFrame:
        """
        Utilizes the trained model to predict back-order status for a given DataFrame.
        """

        logging.info("Entered predict method of BackOrderPredictionModel class")

        try:
            logging.info("Using the trained model to get predictions")

            transformed_feature = self.preprocessing_object.transform(dataframe)

            logging.info("Used the trained model to get predictions")

            return self.trained_model_object.predict(transformed_feature)

        except Exception as e:
            raise BackOrderException(e, sys) from e
        
    def get_original_labels(self,prediction_array: np.array) -> np.array:
        """
        Converts predicted label indices back to their original labels using the label encoder.
        """

        try:
            logging.info('get_original_labels')

            original_labels = self.label_encoder_object.inverse_transform(prediction_array)

            return original_labels
        
        except Exception as e:
            raise BackOrderException(e, sys) from e
        

    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"


