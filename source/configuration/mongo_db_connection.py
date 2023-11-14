import os
import sys

import certifi
import pymongo

from source.constants.database import DATABASE_NAME
from source.constants.env_variable import MONGODB_URL_KEY
from source.exception import BackOrderException

# Get the path to the system's CA file using certifi
ca = certifi.where()

class MongoDBClient:
    """
    MongoDBClient class for managing MongoDB connections.

    Attributes:
        client: MongoDB client instance shared among all instances of MongoDBClient.
        database: MongoDB database instance.
        database_name (str): Name of the MongoDB database.

    Methods:
        __init__(database_name: str = DATABASE_NAME) -> None:
            Initializes the MongoDBClient with the specified database name.

    Example usage:
    ```
    mongo_client = MongoDBClient(database_name="my_database")
    my_collection = mongo_client.database["my_collection"]
    ```
    """

    client = None

    def __init__(self, database_name=DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY)
                if mongo_db_url is None:
                    raise Exception(f"Environment key: {MONGODB_URL_KEY} is not set.")

                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

            self.client = MongoDBClient.client

            self.database = self.client[database_name]

            self.database_name = database_name

        except Exception as e:
            
            raise BackOrderException(e, sys)
