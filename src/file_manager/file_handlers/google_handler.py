import json
import pathlib
from io import BytesIO, StringIO
from typing import Optional

import pandas as pd
from google.cloud import storage

from file_manager.file_handlers.base_handler import BaseHandler


class GoogleHandler(BaseHandler):
    """
    A file handler for reading and writing files to a Google Cloud Storage bucket.
    """

    def __init__(
        self,
        project: str,
        bucket: str,
        path_prefix: str = "",
        client_kwargs: Optional[dict] = None,
    ):
        if client_kwargs is None:
            client_kwargs = {}
        client_kwargs["project"] = project
        self.client = storage.Client(**client_kwargs)
        self.bucket = self.client.bucket(bucket)
        self.path_prefix = path_prefix

    def save_csv(self, data: pd.DataFrame, path: pathlib.Path):
        self.bucket.blob(self._make_path(path)).upload_from_string(
            data.to_csv(index=False),
            "text/csv",
        )

    def load_csv(self, path: pathlib.Path) -> pd.DataFrame:
        blob = self.bucket.blob(self._make_path(path))
        return pd.read_csv(BytesIO(blob.download_as_string()))

    def save_json(self, data: dict, path: pathlib.Path):
        self.bucket.blob(self._make_path(path)).upload_from_string(
            json.dumps(data),
            "application/json",
        )

    def load_json(self, path: pathlib.Path) -> dict:
        blob = self.bucket.blob(self._make_path(path))
        return json.loads(blob.download_as_string())

    def save_parquet(self, data: pd.DataFrame, path: pathlib.Path):
        buffer = BytesIO()
        data.to_parquet(buffer, index=False)
        buffer.seek(0)
        self.bucket.blob(self._make_path(path)).upload_from_file(
            buffer,
            "application/octet-stream",
        )

    def load_parquet(self, path: pathlib.Path) -> pd.DataFrame:
        blob = self.bucket.blob(self._make_path(path))
        return pd.read_parquet(BytesIO(blob.download_as_string()))
