from sklearn.base import TransformerMixin
import numpy as np
from source.utils import read_yaml_file
from source.constants.training_pipeline import SCHEMA_DROP_COLS, SCHEMA_FILE_PATH
from source.exception import BackOrderException
from source.logger import logging
import pandas as pd
## custom class with fit and tranform to perform winsorization

class Winsorizer(TransformerMixin):
    def __init__(self):
        """
        Initialize the Winsorizer transformer.

        Parameters:
        - lower_quantile (float): Lower quantile for winsorization (default: 0.05).
        - upper_quantile (float): Upper quantile for winsorization (default: 0.95).
        """
        # self.change = change

    def fit(self, X, y=None):
        """
        Fit the Winsorizer transformer.

        Parameters:
        - X (array-like): Input data.
        - y: Ignored.

        Returns:
        - self: Returns the instance of the transformer.
        """
        # Calculate the percentiles
        p0 = np.nanpercentile(X, 0)
        p100 = np.nanpercentile(X, 100)

        # Calculate the lower and upper IQR
        Q1 = np.nanpercentile(X, 25)
        Q3 = np.nanpercentile(X, 75)
        IQR = Q3 - Q1

        # Calculate the lower and upper bounds
        self.lower_bound = max(Q1 - (1.5 * IQR),p0)
        self.upper_bound = min(Q3 + (1.5 * IQR),p100)
        return self

    def transform(self, X):
        """
        Transform the input data using winsorization.

        Parameters:
        - X (array-like): Input data to be transformed.

        Returns:
        - X_transformed (array-like): Transformed data after winsorization.
        """

        X_clipped = np.clip(X, self.lower_bound, self.upper_bound)
        return X_clipped

    def get_feature_names_out(self, input_features):
        """
        Get the feature names after transformation.

        Parameters:
        - input_features (array-like): Input feature names.

        Returns:
        - output_features (array-like): Transformed feature names.
        """
        return input_features
    
def drop_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    will drop unneccesary columns before data transformation
     """
    _schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH) 

    df = df.drop(_schema_config[SCHEMA_DROP_COLS], axis=1)

    logging.info(f"Features droped out:{_schema_config[SCHEMA_DROP_COLS]}")

    return df