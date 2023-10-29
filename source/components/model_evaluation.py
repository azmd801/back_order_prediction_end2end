from source.exception import BackOrderException
from source.logger import logging

from source.entity.artifact_entity import (
    DataValidationArtifact,ModelTrainerArtifact,
    ModelEvaluationArtifact,DataTransformationArtifact
    )

from source.entity.config_entity import ModelEvaluationConfig
import os,sys
from source.ml.metric import calculate_metric
from source.ml.estimator import BackOrderPredictionModel
from source.utils import save_object,load_object,write_yaml_file
from source.ml.estimator import ModelResolver
from source.constants.training_pipeline import TARGET_COLUMN
import pandas  as  pd


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
    


    def initiate_model_evaluation(self)->ModelEvaluationArtifact:
        try:
            valid_test_file_path = self.data_validation_artifact.valid_test_file_path

            # valid  test file dataframe
            test_df = pd.read_csv(valid_test_file_path)

            y_true = test_df[TARGET_COLUMN]

            test_df.drop(TARGET_COLUMN,axis=1,inplace=True)
            
            train_model_file_path = self.model_trainer_artifact.trained_model_file_path
            label_encoder_file_path = self.data_transformation_artifact.label_encoder_object_file_path
           
            model_resolver = ModelResolver()

            is_model_accepted=True

            if not model_resolver.is_model_exists():
                model_evaluation_artifact = ModelEvaluationArtifact(
                    is_model_accepted=is_model_accepted, 
                    improved_accuracy=None, 
                    best_model_path=None, 
                    trained_model_path=train_model_file_path, 
                    train_model_metric_artifact=self.model_trainer_artifact.test_metric_artifact, 
                    best_model_metric_artifact=None)
                
                logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")
                
                return model_evaluation_artifact

            latest_model_path = model_resolver.get_best_model_path()
            latest_model = load_object(file_path=latest_model_path)
            train_model = load_object(file_path=train_model_file_path)
            label_encoder = load_object(file_path=label_encoder_file_path)

            y_true = label_encoder.fit_transform(y_true)
            y_trained_pred = train_model.predict(test_df)
            y_latest_pred  =latest_model.predict(test_df)

            trained_metric = calculate_metric(y_true, y_trained_pred)
            latest_metric = calculate_metric(y_true, y_latest_pred)

            improved_accuracy = trained_metric.balanced_accuracy -latest_metric.balanced_accuracy
            if self.model_eval_config.change_threshold < improved_accuracy:
                #0.02 < 0.03
                is_model_accepted=True
            else:
                is_model_accepted=False

            
            model_evaluation_artifact = ModelEvaluationArtifact(
                    is_model_accepted=is_model_accepted, 
                    improved_accuracy=improved_accuracy, 
                    best_model_path=latest_model_path, 
                    trained_model_path=train_model_file_path, 
                    train_model_metric_artifact=trained_metric, 
                    best_model_metric_artifact=latest_metric)

            model_eval_report = model_evaluation_artifact.__dict__

            #save the report
            write_yaml_file(self.model_eval_config.report_file_path, model_eval_report)
            logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")
            return model_evaluation_artifact
            
        except Exception as e:
            raise BackOrderException(e,sys)
