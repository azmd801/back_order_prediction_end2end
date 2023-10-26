from sklearn.metrics import (
    confusion_matrix, f1_score, precision_score, 
    recall_score, balanced_accuracy_score, roc_auc_score
    )

from source.entity.artifact_entity import ClassificationMetricArtifact


def calculate_metric(model, x, y) -> ClassificationMetricArtifact:
    """
    model: estimator
    x: input feature
    y: output feature
    """
    yhat = model.predict(x)

    classification_metric = ClassificationMetricArtifact(
        f1_score=f1_score(y, yhat),
        recall_score=recall_score(y, yhat),
        precision_score=precision_score(y, yhat),
        balanced_accuracy_score=balanced_accuracy_score(y, yhat),
        roc_auc_score=roc_auc_score(y, yhat),
    )

    return classification_metric


# def total_cost(y_true, y_pred):
#     """
#     This function takes y_ture, y_predicted, and prints Total cost due to misclassification
#     """
#     tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()

#     cost = 10 * fp + 500 * fn

#     return cost