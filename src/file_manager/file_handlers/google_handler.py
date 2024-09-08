import json
import pathlib
from io import BytesIO
from typing import Optional

import pandas as pd
from google.cloud import storage

from file_manager.file_handlers.base_handler import BaseHandler


class GoogleHandler(BaseHandler):
    """
    A file handler for reading and writing files to a Google Cloud Storage bucket.

    Implementation Details
    ----------------------
    The handler uses the ``google.cloud.storage`` library to interact with Google Cloud
    Storage. More specifically, it uses the ``google.cloud.storage.Client`` class to
    create a client object that can be used to interact with the GCS bucket. Users can
    supply custom arguments to the ``google.cloud.storage.Client`` instantiation by
    providing them as a dictionary in the ``client_kwargs`` argument of the handler. This
    is useful for supplying custom GCS credentials or other configuration options. For
    more information on authentication to GCS via the ``google.cloud.storage.Client``
    class, visit the google documentation on client library authentication here:
    https://cloud.google.com/docs/authentication/client-libraries

    Parameters
    ----------
    project : str
        The name of the GCP project to use for authentication.
    bucket : str
        The name of the GCS bucket to read and write files from.
    path_prefix : str, optional
        A prefix to add to the start of all file paths. This can be used to store files
        in a subdirectory within the bucket. Typically, this would be a directory name
        that matches the project name.
    client_kwargs : dict, optional
        Additional keyword arguments to pass to the google.cloud.storage.Client when
        connecting to GCS.

    Examples
    --------
    >>> from file_manager.file_handlers import GoogleHandler
    >>> # Setup a Google Cloud Storage handler using Application Default Credentials (ADC)
    >>> gcs_handler = GoogleHandler(
    ...     project="my-project", bucket="my-bucket", path_prefix="my_sub_project/"
    ... )
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
