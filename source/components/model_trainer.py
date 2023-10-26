import sys

# from neuro_mf import ModelFactory

from source.entity.artifact_entity import (
    DataTransformationArtifact,
    ModelTrainerArtifact,
    ClassificationMetricArtifact
)
from source.entity.config_entity import ModelTrainerConfig
from source.exception import BackOrderException
from source.logger import logging
from source.ml import metric
from source.ml.estimator import BackOrderPredictionModel
from source.utils import load_numpy_array_data, load_object, save_object
from source.ml.model import TunedModel
from source.ml.metric import calculate_metric


class ModelTrainer:
    def __init__(
        self,
        data_transformation_artifact: DataTransformationArtifact,
        model_trainer_config: ModelTrainerConfig,
    ):
        self.data_transformation_artifact = data_transformation_artifact

        self.model_trainer_config = model_trainer_config

    def initiate_model_trainer(self,) -> ModelTrainerArtifact:
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")

        try:
            train_arr = load_numpy_array_data(
                file_path=self.data_transformation_artifact.transformed_train_file_path
            )

            test_arr = load_numpy_array_data(
                file_path=self.data_transformation_artifact.transformed_test_file_path
            )

            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )

            model= TunedModel().initiate_model()

            model.fit(x_train,y_train)

            model_metrics : ClassificationMetricArtifact  = calculate_metric(model,x_test,y_test)

            if (
                model_metrics.balanced_accuracy_score < self.model_trainer_config.expected_accuracy
            ):
                logging.info("No best model found with score more than base score")

                raise Exception("No best model found with score more than base score")
            
            preprocessing_obj = load_object(
                file_path=self.data_transformation_artifact.preprocessor_object_file_path
            )

            backOrder_prediction_model = BackOrderPredictionModel(
                preprocessing_object=preprocessing_obj,
                trained_model_object=model,
            )

            logging.info(
                "Created Back oreder prediction model object with preprocessor and model"
            )

            logging.info("Created best model file path.")

            save_object(self.model_trainer_config.trained_model_file_path, backOrder_prediction_model)

            metric_artifact = calculate_metric(
                model=model, x=x_test, y=y_test
            )

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                metric_artifact=metric_artifact,
            )

            logging.info(f"Model trainer artifact: {model_trainer_artifact}")

            return model_trainer_artifact

        except Exception as e:
            raise BackOrderException(e, sys) from e


