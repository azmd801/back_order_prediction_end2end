import sys

from source.components.data_ingestion import DataIngestion
from source.components.data_transformation import DataTransformation
from source.components.data_validation import DataValidation
from source.components.model_evaluation import ModelEvaluation
from source.components.model_pusher import ModelPusher
from source.components.model_trainer import ModelTrainer
from source.entity.artifact_entity import (
    DataIngestionArtifact,
    DataTransformationArtifact,
    DataValidationArtifact,
    ModelEvaluationArtifact,
    ModelTrainerArtifact,
)
from source.entity.config_entity import (
    DataIngestionConfig,
    DataTransformationConfig,
    DataValidationConfig,
    ModelEvaluationConfig,
    ModelPusherConfig,
    ModelTrainerConfig,
)
from source.exception import BackOrderException
from source.logger import logging


class TrainPipeline:

    """
    This class represents the end-to-end training pipeline for the BackOrder prediction model.

    Methods:
        start_data_ingestion() -> DataIngestionArtifact:
            Start the data ingestion process and return the data ingestion artifact.

        start_data_validation(data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
            Start the data validation process and return the data validation artifact.

        start_data_transformation(data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
            Start the data transformation process and return the data transformation artifact.

        start_model_trainer(data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
            Start the model training process and return the model trainer artifact.

        start_model_evaluation(data_validation_artifact: DataValidationArtifact,
                               data_transformation_artifact: DataTransformationArtifact,
                               model_trainer_artifact: ModelTrainerArtifact) -> ModelEvaluationArtifact:
            Start the model evaluation process and return the model evaluation artifact.

        start_model_pusher(model_trainer_artifact: ModelTrainerArtifact):
            Start the model pushing process.

        run_pipeline():
            Run the entire training pipeline.

    Attributes:
        data_ingestion_config (DataIngestionConfig): Data ingestion configuration.
        data_validation_config (DataValidationConfig): Data validation configuration.
        data_transformation_config (DataTransformationConfig): Data transformation configuration.
        model_trainer_config (ModelTrainerConfig): Model trainer configuration.
        model_evaluation_config (ModelEvaluationConfig): Model evaluation configuration.
        model_pusher_config (ModelPusherConfig): Model pusher configuration.
    """

    def __init__(self):
        """
        Initialize TrainPipeline instance with default configurations.
        """

        self.data_ingestion_config = DataIngestionConfig()

        self.data_validation_config = DataValidationConfig()

        self.data_transformation_config = DataTransformationConfig()

        self.model_trainer_config = ModelTrainerConfig()

        self.model_evaluation_config = ModelEvaluationConfig()

        self.model_pusher_config = ModelPusherConfig()


    def start_data_ingestion(self)-> DataIngestionArtifact:
        try:
            logging.info(
                "Entered the start_data_ingestion method of TrainPipeline class"
            )

            logging.info("Getting the data from mongodb")

            data_ingestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config
            )

            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

            logging.info("Got the train_set and test_set from mongodb")

            logging.info(
                "Exited the start_data_ingestion method of TrainPipeline class"
            )

            return data_ingestion_artifact

        except Exception as e:
            raise BackOrderException(e, sys) from e
 

    def start_data_validation(
        self, data_ingestion_artifact: DataIngestionArtifact
    ) -> DataValidationArtifact:
        """
        Start the data validation process.
        """

        logging.info("Entered the start_data_validation method of TrainPipeline class")

        try:
            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=self.data_validation_config,
            )

            data_validation_artifact = data_validation.initiate_data_validation()

            logging.info("Performed the data validation operation")

            logging.info(
                "Exited the start_data_validation method of TrainPipeline class"
            )

            return data_validation_artifact

        except Exception as e:
            raise BackOrderException(e, sys) from e

    def start_data_transformation(
        self, data_validation_artifact: DataValidationArtifact
    ) -> DataTransformationArtifact:
        """
        Start the data transformation process.
        """

        try:
            data_transformation = DataTransformation(
                data_validation_artifact, self.data_transformation_config
            )

            data_transformation_artifact = (
                data_transformation.initiate_data_transformation()
            )

            return data_transformation_artifact

        except Exception as e:
            raise BackOrderException(e, sys)
 

    def start_model_trainer(
        self, data_transformation_artifact: DataTransformationArtifact
    ) -> ModelTrainerArtifact:
        """
        Start the model training process.
        """
        
        try:
            model_trainer = ModelTrainer(
                data_transformation_artifact=data_transformation_artifact,
                model_trainer_config=self.model_trainer_config,
            )

            model_trainer_artifact = model_trainer.initiate_model_trainer()

            return model_trainer_artifact

        except Exception as e:
            raise BackOrderException(e, sys) 
        
    def start_model_evaluation(
        self,
        data_validation_artifact: DataValidationArtifact,
        data_transformation_artifact:DataTransformationArtifact,
        model_trainer_artifact: ModelTrainerArtifact,
    ) -> ModelEvaluationArtifact:
        """
        Start the model evaluation process.
        """

        try:
            model_evaluation = ModelEvaluation(
                model_eval_config=self.model_evaluation_config,
                data_validation_artifact=data_validation_artifact,
                data_transformation_artifact=data_transformation_artifact,
                model_trainer_artifact=model_trainer_artifact,
            )

            model_evaluation_artifact = model_evaluation.initiate_model_evaluation()

            return model_evaluation_artifact

        except Exception as e:
            raise BackOrderException(e, sys)


    def start_model_pusher(self, model_trainer_artifact: ModelTrainerArtifact):
        """
        Start the model pushing process.
        """

        try:
            model_pusher = ModelPusher(
                model_pusher_config=self.model_pusher_config,
                model_trainer_artifact = model_trainer_artifact
            )

            model_pusher_artifact = model_pusher.initiate_model_pusher()

            return model_pusher_artifact
        
        except Exception as e:
            raise BackOrderException(e, sys) 

    def run_pipeline(self):
        """
        Run the entire training pipeline.
        """
        
        try:
            data_ingestion_artifact: DataIngestionArtifact = self.start_data_ingestion()
            
            data_validation_artifact = self.start_data_validation(
                data_ingestion_artifact
            )      

            data_transformation_artifact = self.start_data_transformation(
                data_validation_artifact
            )      

            model_trainer_artifact = self.start_model_trainer(
                data_transformation_artifact
            )
            model_evaluation_artifact = self.start_model_evaluation(
                data_validation_artifact, data_transformation_artifact, model_trainer_artifact,
            )

            if not model_evaluation_artifact.is_model_accepted:
                logging.info(f"Model not accepted.")

                logging.info(f"Exiting the training pipeline")

                return None   
            
            model_pusher_artifact = self.start_model_pusher(
                model_trainer_artifact=model_trainer_artifact
            )

            logging.info(f"Exiting the training pipeline")         

        except Exception as e:
            raise BackOrderException(e, sys) from e     