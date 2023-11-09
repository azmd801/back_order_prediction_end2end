# pipeline name and root directory constant
import os

from source.constants.s3_bucket import TRAINING_BUCKET_NAME

TARGET_COLUMN = "went_on_backorder"

PIPELINE_NAME: str = "back_order_prediction"

ARTIFACT_DIR: str = "artifact"

SAVED_MODEL_DIR: str = os.path.join("saved_models")

# common file name

FILE_NAME: str = "back_order.csv"

TRAIN_FILE_NAME: str = "train.csv"

TEST_FILE_NAME: str = "test.csv"

PREPROCSSING_OBJECT_FILE_NAME = "preprocessing.pkl"

LABEL_ENCODER_OBJECT_FILE_NAME = "label_encoder.pkl"

MODEL_FILE_NAME = "model.pkl"

SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")

MODEL_CONFIG_FILE_PATH = os.path.join("config", "model.yaml")

PREPROCESSING_CONFIG_FILE_PATH = os.path.join("config","preprocessing.yaml")

SCHEMA_DROP_COLS = "drop_columns"

"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""
DATA_INGESTION_COLLECTION_NAME: str = "back_orders"

DATA_INGESTION_DIR_NAME: str = "data_ingestion"

DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"

DATA_INGESTION_INGESTED_DIR: str = "ingested"

DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2

"""
Data Validation realted contant start with DATA_VALIDATION VAR NAME
"""

DATA_VALIDATION_DIR_NAME: str = "data_validation"

DATA_VALIDATION_VALID_DIR: str = "validated"

DATA_VALIDATION_INVALID_DIR: str = "invalid"

DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"

DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"

"""
Data Transformation ralated constant start with DATA_TRANSFORMATION VAR NAME
"""

DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"

DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"

DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"

"""
MODEL TRAINER related constant start with MODEL_TRAINER var name
"""
MODEL_TRAINER_DIR_NAME: str = "model_trainer"

MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"

MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"

MODEL_TRAINER_EXPECTED_SCORE: float = 0.0

MODEL_TRAINER_MODEL_CONFIG_FILE_PATH: str = os.path.join("config", "model.yaml")


"""
model relted constants
"""
MODULE_OF_MODEL = 'module'

CLASS_OF_MODEL = 'class'

TUNED_PARAMS_OF_MODEL = 'params'




"""
Model evaluation ralated constant 
"""

MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE: float = 0.02

MODEL_PUSHER_BUCKET_NAME = TRAINING_BUCKET_NAME

MODEL_PUSHER_S3_KEY = "model-registry"

"""
Model pusher ralated constant 
"""
MODEL_PUSHER_DIR_NAME = "model_pusher"
MODEL_PUSHER_SAVED_MODEL_DIR = SAVED_MODEL_DIR



