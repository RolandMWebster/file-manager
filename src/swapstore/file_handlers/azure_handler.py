import io
import json
import pathlib
import pickle
from typing import Any, Optional

import pandas as pd

from swapstore.file_handlers.base_handler import BaseHandler


class AzureHandler(BaseHandler):
    """
    A file handler for reading and writing files to an Azure Blob Storage container.

    Implementation Details
    ----------------------
    The handler uses the ``azure.storage.blob.BlobServiceClient`` class to interact
    with an Azure Blob Storage container. By default, the handler uses the
    azure.identity.DefaultAzureCredential class for authentication.

    Parameters
    ----------
    account_url : str
        The URL of the Azure Blob Storage account to connect to.
    container : str
        The name of the container to read and write files from.
    path_prefix : str, optional
        A prefix to add to the start of all file paths. This can be used to store files
        in a subdirectory within the container. Typically, this would be a directory name
        that matches the project name.
    client_kwargs : dict, optional
        Additional keyword arguments to pass to the azure.storage.blob.BlobServiceClient
        when connecting to Azure Blob Storage.

    Examples
    --------
    >>> from file_manager.file_handlers import AzureHandler
    >>> # Setup an Azure Blob Storage handler
    >>> azure_handler = AzureHandler(
    ...     account_url="https://myaccount.blob.core.windows.net",
    ...     container="my-container",
    ...     path_prefix="my_project/"
    ... )
    """

    def __init__(
        self,
        account_url: str,
        container: str,
        path_prefix: str = "",
        client_kwargs: Optional[dict] = None,
    ):
        try:
            from azure.identity import DefaultAzureCredential  # type: ignore
            from azure.storage.blob import BlobServiceClient  # type: ignore
        except ImportError:
            raise ImportError(
                "Azure Blob Storage dependencies are not installed. "
                "Please install via pip install file_manager[azure]."
            )
        if client_kwargs is None:
            client_kwargs = {}
        client_kwargs["account_url"] = account_url
        if "credential" not in client_kwargs:
            client_kwargs["credential"] = DefaultAzureCredential()
        self.client = BlobServiceClient(**client_kwargs)
        self.container = container
        self.path_prefix = path_prefix

    def _make_path(self, path: pathlib.Path) -> str:
        # return string with prefix in front
        path_with_prefix = pathlib.Path(self.path_prefix) / path
        return str(path_with_prefix)

    def save_csv(self, data: pd.DataFrame, path: pathlib.Path):
        blob_client = self.client.get_blob_client(
            container=self.container, blob=self._make_path(path)
        )
        blob_client.upload_blob(data.to_csv(index=False), overwrite=True)

    def load_csv(self, path: pathlib.Path) -> pd.DataFrame:
        blob_client = self.client.get_blob_client(
            container=self.container, blob=self._make_path(path)
        )
        csv_data = io.StringIO(blob_client.download_blob().readall().decode("utf-8"))
        return pd.read_csv(csv_data)

    def save_json(self, data: dict, path: pathlib.Path):
        blob_client = self.client.get_blob_client(
            container=self.container, blob=self._make_path(path)
        )
        blob_client.upload_blob(json.dumps(data), overwrite=True)

    def load_json(self, path: pathlib.Path) -> dict:
        blob_client = self.client.get_blob_client(
            container=self.container, blob=self._make_path(path)
        )
        return json.loads(blob_client.download_blob().readall())

    def save_parquet(self, data: pd.DataFrame, path: pathlib.Path):
        blob_client = self.client.get_blob_client(
            container=self.container, blob=self._make_path(path)
        )
        blob_client.upload_blob(data.to_parquet(), overwrite=True)

    def load_parquet(self, path: pathlib.Path) -> pd.DataFrame:
        blob_client = self.client.get_blob_client(
            container=self.container, blob=self._make_path(path)
        )
        return pd.read_parquet(io.BytesIO(blob_client.download_blob().readall()))

    def save_pickle(self, data: Any, path: pathlib.Path):
        blob_client = self.client.get_blob_client(
            container=self.container, blob=self._make_path(path)
        )
        blob_client.upload_blob(pickle.dumps(data), overwrite=True)

    def load_pickle(self, path: pathlib.Path) -> Any:
        blob_client = self.client.get_blob_client(
            container=self.container, blob=self._make_path(path)
        )
        return pickle.loads(blob_client.download_blob().readall())
