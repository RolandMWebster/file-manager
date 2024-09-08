import json
import pathlib
from io import BytesIO, StringIO
from typing import Optional

import boto3
import pandas as pd

from file_manager.file_handlers.base_handler import BaseHandler


class S3Handler(BaseHandler):
    """
    A file handler for reading and writing files to an S3 bucket.

    Implementation Details
    ----------------------
    The handler uses the `boto3` library to interact with S3. More specifically, it uses
    the `boto3.client` method to create a client object that can be used to interact with
    the S3 bucket. Users can supply custom arguments to the `boto3.client` instantiation
    by providing them as a dictionary in the `client_kwargs` argument of the handler.
    This is useful for supplying custom AWS credentials or other configuration options.
    For more information on authentication to AWS services via the `boto3.client` method,
    visit the boto3 documentation here:
    https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html

    Parameters
    ----------
    bucket : str
        The name of the S3 bucket to read and write files from.
    path_prefix : str, optional
        A prefix to add to the start of all file paths. This can be used to store files
        in a subdirectory within the bucket. Typically, this would be a directory name
        that matches the project name.
    client_kwargs : dict, optional
        Additional keyword arguments to pass to the boto3 client when connecting to S3.

    Examples
    --------
    >>> from file_manager.file_handlers import S3Handler
    >>> # Setup an S3 handler using default AWS credentials stored in ~/.aws/credentials
    >>> s3_handler = S3Handler(bucket="my-bucket", path_prefix="my_project/")
    >>> # Setup an S3 handler using custom AWS credentials
    >>> s3_handler_custom_creds = S3Handler(
    ...     bucket="my-bucket",
    ...     path_prefix="my_project/",
    ...     client_kwargs={
    ...         "aws_access_key_id": "my_access_key_id",
    ...         "aws_secret_access_key": "my_secret_access_key",
    ...     }
    ... )
    """

    def __init__(
        self, bucket: str, path_prefix: str = "", client_kwargs: Optional[dict] = None
    ):
        if client_kwargs is None:
            client_kwargs = {}
        client_kwargs["service_name"] = "s3"  # force service name to be 's3'
        self.client_kwargs = client_kwargs
        self.client = boto3.client(**client_kwargs)
        self.bucket = bucket
        self.path_prefix = path_prefix
        self._check_read_access()

    def _make_path(self, path: pathlib.Path) -> str:
        # return string with prefix in front
        path_with_prefix = pathlib.Path(self.path_prefix) / path
        return str(path_with_prefix)

    def _check_read_access(self):
        try:
            # Attempt to list objects in the bucket
            self.client.list_objects_v2(Bucket=self.bucket, MaxKeys=1)
        except self.client.exceptions.ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "AccessDenied":
                raise (f"Read access to bucket '{self.bucket}' is denied.")
            else:
                print(f"An error occurred: {e}")

    def save_csv(self, data: pd.DataFrame, path: pathlib.Path):
        buffer = StringIO()
        data.to_csv(buffer, index=False)
        self.client.put_object(
            Bucket=self.bucket, Key=self._make_path(path), Body=buffer.getvalue()
        )

    def load_csv(self, path: pathlib.Path) -> pd.DataFrame:
        response = self.client.get_object(Bucket=self.bucket, Key=self._make_path(path))
        return pd.read_csv(response["Body"])

    def save_parquet(self, data: pd.DataFrame, path: pathlib.Path):
        buffer = BytesIO()
        data.to_parquet(buffer, index=False, engine="pyarrow")
        self.client.put_object(
            Bucket=self.bucket, Key=self._make_path(path), Body=buffer.getvalue()
        )

    def load_parquet(self, path: pathlib.Path) -> pd.DataFrame:
        response = self.client.get_object(Bucket=self.bucket, Key=self._make_path(path))
        return pd.read_parquet(BytesIO(response["Body"].read()))

    def save_json(self, data: dict, path: pathlib.Path):
        self.client.put_object(
            Bucket=self.bucket, Key=self._make_path(path), Body=json.dumps(data)
        )

    def load_json(self, path: pathlib.Path) -> dict:
        response = self.client.get_object(Bucket=self.bucket, Key=self._make_path(path))
        return json.loads(response["Body"].read().decode("utf-8"))
