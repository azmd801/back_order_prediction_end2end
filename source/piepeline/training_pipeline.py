import sys

# from source.components.data_ingestion import DataIngestion
# from source.components.data_transformation import DataTransformation
# from source.components.data_validation import DataValidation
# from source.components.model_evaluation import ModelEvaluation
# from source.components.model_pusher import ModelPusher
# from source.components.model_trainer import ModelTrainer
# from source.entity.artifact_entity import (
#     DataIngestionArtifact,
#     DataTransformationArtifact,
#     DataValidationArtifact,
#     ModelEvaluationArtifact,
#     ModelTrainerArtifact,
# )
from source.entity.config_entity import (
    DataIngestionConfig
    # DataTransformationConfig,
    # DataValidationConfig,
    # ModelEvaluationConfig,
    # ModelPusherConfig,
    # ModelTrainerConfig,
)
from source.exception import BackOrderException
from source.logger import logging


class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()

        # self.data_validation_config = DataValidationConfig()

        # self.data_transformation_config = DataTransformationConfig()

        # self.model_trainer_config = ModelTrainerConfig()

        # self.model_evaluation_config = ModelEvaluationConfig()

        # self.model_pusher_config = ModelPusherConfig()

    def start_data_ingestion(self):
        try:
            pass
        except Exception as e:
            raise BackOrderException(e, sys) from e


    def start_data_ingestion(self):
        try:
            pass
        except Exception as e:
            raise BackOrderException(e, sys) from e 

    def start_data_validation(self):
        try:
            pass
        except Exception as e:
            raise BackOrderException(e, sys) from e

    def start_data_trasformation(self):
        try:
            pass
        except Exception as e:
            raise BackOrderException(e, sys) from e   

    def start_model_trainer(self):
        try:
            pass
        except Exception as e:
            raise BackOrderException(e, sys) from e  

    def start_model_pusher(self):
        try:
            pass
        except Exception as e:
            raise BackOrderException(e, sys) from e  

    def run_pipeline(self):
        try:
            pass
        except Exception as e:
            raise BackOrderException(e, sys) from e     