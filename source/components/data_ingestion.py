import os
import sys

from pandas import DataFrame
from sklearn.model_selection import train_test_split

from source.constants.training_pipeline import SCHEMA_DROP_COLS, SCHEMA_FILE_PATH
from source.data_access.back_order_data import BackOrderData
from source.entity.artifact_entity import DataIngestionArtifact
from source.entity.config_entity import DataIngestionConfig
from source.exception import BackOrderException
from source.logger import logging
from source.utils import read_yaml_file


class DataIngestion:
    """
    Class for ingesting data from MongoDB, exporting it to a feature store, 
    and splitting it into training and testing datasets.

    Attributes:
        data_ingestion_config (DataIngestionConfig): Configuration for data ingestion.

    Methods:
        export_data_into_feature_store() -> DataFrame:
            Export data from MongoDB to a feature store file.

        split_data_as_train_test(dataframe: DataFrame) -> None:
            Split the given dataframe into training and testing datasets and export them.

        initiate_data_ingestion() -> DataIngestionArtifact:
            Initiates the data ingestion process, including exporting and splitting data.
    """


    def __init__(
        self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()
    ):
        """
        Initialize the DataIngestion instance
        """

        try:
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise BackOrderException(e, sys)

    def export_data_into_feature_store(self) -> DataFrame:
        """
        Export data from MongoDB to a feature store file.
        """

        try:
            logging.info(f"Exporting data from mongodb")

            back_order_data = BackOrderData()

            dataframe = back_order_data.export_collection_as_dataframe(
                collection_name=self.data_ingestion_config.collection_name
            )

            logging.info(f"Shape of dataframe: {dataframe.shape}")

            feature_store_file_path = self.data_ingestion_config.feature_store_file_path

            dir_path = os.path.dirname(feature_store_file_path)

            os.makedirs(dir_path, exist_ok=True)

            logging.info(
                f"Saving exported data into feature store file path: {feature_store_file_path}"
            )

            dataframe.to_csv(feature_store_file_path, index=False, header=True)

            return dataframe

        except Exception as e:
            raise BackOrderException(e, sys)
        
    def split_data_as_train_test(self, dataframe: DataFrame) -> None:
        """
        Split the given dataframe into training and testing datasets and export them.
        """

        logging.info("Entered split_data_as_train_test method of Data_Ingestion class")

        try:
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )

            logging.info("Performed train test split on the dataframe")

            logging.info(
                "Exited split_data_as_train_test method of Data_Ingestion class"
            )

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)

            os.makedirs(dir_path, exist_ok=True)

            logging.info(f"Exporting train and test file path.")

            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )

            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )

            logging.info(f"Exported train and test file path.")

        except Exception as e:
            raise BackOrderException(e, sys) from e

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Initiates the data ingestion process, including exporting and splitting data.
        """
        
        logging.info("Entered initiate_data_ingestion method of Data_Ingestion class")
        try: 
            if not (os.path.isfile(self.data_ingestion_config.training_file_path) and \
                    os.path.isfile(self.data_ingestion_config.testing_file_path)):
                              
                dataframe = self.export_data_into_feature_store()

                logging.info("Got the data from mongodb")
           
                self.split_data_as_train_test(dataframe)

                logging.info("Performed train test split on the dataset")

                logging.info(
                "Exited initiate_data_ingestion method of Data_Ingestion class"
                )
            else:
                logging.info("Dataset already available")

            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path,
            )

            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")

            return data_ingestion_artifact
        
        except Exception as e:
            raise BackOrderException(e, sys) from e  

        
