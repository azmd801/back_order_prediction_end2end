from source.exception import BackOrderException
from source.logger import logging

from source.entity.artifact_entity import (
    DataValidationArtifact,ModelTrainerArtifact,
    ModelEvaluationArtifact,DataTransformationArtifact,
    ClassificationMetricArtifact  
    )

from source.entity.config_entity import ModelEvaluationConfig
import os,sys
from source.ml.metric import calculate_metric
from source.ml.estimator import BackOrderPredictionModel
from source.utils import save_object,load_object,write_yaml_file
from source.ml.s3_estimator import BackOrderEstimator
from source.constants.training_pipeline import *
import pandas  as  pd
from typing import Optional

class ModelEvaluation:


    def __init__(self,model_eval_config:ModelEvaluationConfig,
                    data_validation_artifact:DataValidationArtifact,
                    data_transformation_artifact:DataTransformationArtifact,
                    model_trainer_artifact:ModelTrainerArtifact):
        
        try:
            self.model_eval_config=model_eval_config
            self.data_validation_artifact=data_validation_artifact
            self.model_trainer_artifact=model_trainer_artifact
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise BackOrderException(e,sys)
        
    def get_best_model(self) -> Optional[BackOrderEstimator]:
        try:
            bucket_name = self.model_eval_config.bucket_name

            model_path = self.model_eval_config.s3_model_key_path

            back_order_estimator = BackOrderEstimator(
                bucket_name=bucket_name, model_path=model_path
            )

            if back_order_estimator.is_model_present(model_path=model_path):
                return back_order_estimator

            return None

        except Exception as e:
            raise BackOrderException(e, sys)
    
    def evaluate_model(self) -> bool:
        try:
            test_df = pd.read_csv(self.data_validation_artifact.valid_test_file_path)

            x, y = test_df.drop(TARGET_COLUMN, axis=1), test_df[TARGET_COLUMN]

            trained_model = load_object(
                file_path=self.model_trainer_artifact.trained_model_file_path
            )
            label_encoder = load_object(
                file_path=self.data_transformation_artifact.label_encoder_object_file_path
            )

            y = label_encoder.fit_transform(y)

            trained_model_score : ClassificationMetricArtifact = calculate_metric(trained_model, x, y)

            trained_model_balanced_accuracy = trained_model_score.balanced_accuracy_score


            best_model = self.get_best_model()

            if best_model is None:
                is_model_accepted=True

            else:

                best_model_score = calculate_metric(best_model, x, y)

                best_model_balanced_accuracy = best_model_score.balanced_accuracy_score

                is_model_accepted = trained_model_balanced_accuracy - best_model_balanced_accuracy\
                      > MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE

                logging.info(f"Trained model balanced accuracy = {trained_model_balanced_accuracy}" )
                logging.info(f"Previous best model balanced accuracy = {best_model_balanced_accuracy}" )                
                             
            return is_model_accepted

        except Exception as e:
            raise BackOrderException(e, sys)

    def initiate_model_evaluation(self)->ModelEvaluationArtifact:
        try:

            model_evaluation_artifact = ModelEvaluationArtifact(
                is_model_accepted = self.evaluate_model()
            )

            return model_evaluation_artifact
            
        except Exception as e:
            raise BackOrderException(e,sys)
