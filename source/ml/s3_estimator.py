import sys

from pandas import DataFrame

from source.cloud_storage.aws_storage import SimpleStorageService
from source.exception import BackOrderException
from source.ml.estimator import BackOrderPredictionModel


class BackOrderEstimator:
    """
    This class is used to save and retrieve a model in an S3 bucket and perform predictions.
    """

    def __init__(
        self, bucket_name, model_path,
    ):
        """

        """
        self.bucket_name = bucket_name

        self.s3 = SimpleStorageService()

        self.model_path = model_path

        self.loaded_model: BackOrderPredictionModel = None


    def is_model_present(self, model_path: str) -> bool:
        """
        Check if the model is present in the specified S3 bucket.
        """
        try:
            return self.s3.s3_key_path_available(
                bucket_name=self.bucket_name, s3_key=model_path
            )

        except BackOrderException as e:
            print(e)

            return False

    def load_model(self,) -> BackOrderPredictionModel:
        """
        Load the model from the specified S3 bucket.
        """

        return self.s3.load_model(self.model_path, bucket_name=self.bucket_name)

    def save_model(self, from_file, remove: bool = False) -> None:
        """
        Save the model to the specified S3 bucket.
        """
        
        try:
            self.s3.upload_file(
                from_file,
                to_filename=self.model_path,
                bucket_name=self.bucket_name,
                remove=remove,
            )

        except Exception as e:
            raise BackOrderException(e, sys)

    
