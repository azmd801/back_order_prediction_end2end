from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    trained_file_path: str

    test_file_path: str

@dataclass
class DataValidationArtifact:
    validation_status: bool

    valid_train_file_path: str

    valid_test_file_path: str

    invalid_train_file_path: str

    invalid_test_file_path: str

    drift_report_file_path: str

@dataclass
class DataTransformationArtifact:
    preprocessor_object_file_path: str
    
    label_encoder_object_file_path: str

    transformed_train_file_path: str

    transformed_test_file_path: str

@dataclass
class ClassificationMetricArtifact:
    f1_score: float

    precision_score: float

    recall_score: float

    balanced_accuracy_score: float

    roc_auc_score: float

@dataclass
class ModelTrainerArtifact:
    trained_model_file_path: str

    train_metric_artifact: ClassificationMetricArtifact

    test_metric_artifact: ClassificationMetricArtifact

@dataclass
class ModelEvaluationArtifact:
    is_model_accepted: bool



@dataclass
class ModelPusherArtifact:
    bucket_name: str

    s3_model_path: str