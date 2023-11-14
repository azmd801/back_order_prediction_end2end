import os

import boto3

from source.constants.env_variable import (
    AWS_ACCESS_KEY_ID_ENV_KEY,
    AWS_SECRET_ACCESS_KEY_ENV_KEY,
    REGION_NAME,
)


class S3Client:

    """
    S3Client class for managing Amazon S3 connections.

    Attributes:
        s3_client: Boto3 S3 client instance.
        s3_resource: Boto3 S3 resource instance.

    Methods:
        __init__(region_name: str = REGION_NAME) -> None:
            Initializes the S3Client with the specified AWS region.

    Example usage:
    ```
    s3_client = S3Client(region_name="us-west-2")
    bucket_list = s3_client.s3_resource.buckets.all()
    ```

    Note:
    - AWS credentials are obtained from the environment variables: AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.
    - If credentials are not set, an exception is raised during initialization.
    - The initialized S3 client and resource instances are shared among all instances of the S3Client class.
    """
    
    s3_client = None
    s3_resource = None

    def __init__(self, region_name=REGION_NAME):

        if S3Client.s3_resource == None or S3Client.s3_client == None:
            __access_key_id = os.getenv(AWS_ACCESS_KEY_ID_ENV_KEY,)

            __secret_access_key = os.getenv(AWS_SECRET_ACCESS_KEY_ENV_KEY,)

            if __access_key_id is None:
                raise Exception(
                    f"Environment variable: {AWS_ACCESS_KEY_ID_ENV_KEY} is not not set."
                )

            if __secret_access_key is None:
                raise Exception(
                    f"Environment variable: {AWS_SECRET_ACCESS_KEY_ENV_KEY} is not set."
                )

            S3Client.s3_resource = boto3.resource(
                "s3",
                aws_access_key_id=__access_key_id,
                aws_secret_access_key=__secret_access_key,
                region_name=region_name,
            )

            S3Client.s3_client = boto3.client(
                "s3",
                aws_access_key_id=__access_key_id,
                aws_secret_access_key=__secret_access_key,
                region_name=region_name,
            )

        self.s3_resource = S3Client.s3_resource

        self.s3_client = S3Client.s3_client
