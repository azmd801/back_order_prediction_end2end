import sys

from source.entity.artifact_entity import ModelPusherArtifact, ModelTrainerArtifact
from source.entity.config_entity import ModelPusherConfig
from source.exception import BackOrderException
from source.logger import logging
from source.ml.s3_estimator import BackOrderEstimator


class ModelPusher:
    """
    This class is responsible for evaluating and comparing the trained model's performance.

    Args:
        model_eval_config (ModelEvaluationConfig): Model evaluation configuration.
        data_validation_artifact (DataValidationArtifact): Data validation artifact.
        data_transformation_artifact (DataTransformationArtifact): Data transformation artifact.
        model_trainer_artifact (ModelTrainerArtifact): Model trainer artifact.

    Methods:
        get_best_model() -> Optional[BackOrderEstimator]:
            Retrieve the best model from the specified S3 bucket.

        evaluate_model() -> bool:
            Evaluate the performance of the trained model and compare it with the best model.

        initiate_model_evaluation() -> ModelEvaluationArtifact:
            Initiate the model evaluation process and return the model evaluation artifact.

    """

    def __init__(
        self,
        model_trainer_artifact: ModelTrainerArtifact,
        model_pusher_config: ModelPusherConfig,
    ):
        """
        Initialize ModelEvaluation instance.
        """

        self.model_trainer_artifact = model_trainer_artifact

        self.model_pusher_config = model_pusher_config

        self.back_order_estimator = BackOrderEstimator(
            bucket_name=model_pusher_config.bucket_name,
            model_path=model_pusher_config.s3_model_key_path,
        )

    def initiate_model_pusher(self) -> ModelPusherArtifact:
        """
        Retrieve the best model from the specified S3 bucket.
        """
        
        logging.info("Entered initiate_model_pusher method of ModelTrainer class")

        try:
            logging.info("Uploading artifacts folder to s3 bucket")

            self.back_order_estimator.save_model(
                from_file=self.model_trainer_artifact.trained_model_file_path
            )

            model_pusher_artifact = ModelPusherArtifact(
                bucket_name=self.model_pusher_config.bucket_name,
                s3_model_path=self.model_pusher_config.s3_model_key_path,
            )

            logging.info("Uploaded artifacts folder to s3 bucket")

            logging.info(f"Model pusher artifact: [{model_pusher_artifact}]")

            logging.info("Exited initiate_model_pusher method of ModelTrainer class")

            return model_pusher_artifact

        except Exception as e:
            raise BackOrderException(e, sys) from e
