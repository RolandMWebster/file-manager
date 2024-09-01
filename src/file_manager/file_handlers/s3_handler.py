import json
import pathlib
from io import BytesIO, StringIO

import boto3
import pandas as pd

from file_manager.file_handlers.base_handler import BaseHandler


class S3Handler(BaseHandler):

    def __init__(self, bucket: str, path_prefix: str = ""):
        self.client = boto3.client("s3")
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
