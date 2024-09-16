import json
import logging
import pathlib
import pickle
from typing import Any

import pandas as pd

from file_manager.file_handlers.base_handler import BaseHandler

logger = logging.getLogger(__name__)


class LocalHandler(BaseHandler):
    """
    A file handler for reading and writing files to the local filesystem.

    Examples
    --------
    >>> from file_manager.file_handlers import LocalHandler
    >>> # setup a local handler
    >>> local_handler = LocalHandler()
    """

    def __init__(self):
        pass

    def make_directory(self, directory: pathlib.Path):
        if not directory.is_dir():
            raise ValueError("The 'directory' argument must be a proper directory.")
        directory.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Directory created at {directory}")

    def save_csv(self, data: pd.DataFrame, path: pathlib.Path):
        data.to_csv(path, index=False)

    def load_csv(self, path: str) -> pd.DataFrame:
        return pd.read_csv(path)

    def save_parquet(self, data: pd.DataFrame, path: pathlib.Path):
        data.to_parquet(path)

    def load_parquet(self, path: pathlib.Path) -> pd.DataFrame:
        return pd.read_parquet(path)

    def save_json(self, data: dict, path: pathlib.Path):
        with open(path, "w") as f:
            json.dump(data, f)

    def load_json(self, path: pathlib.Path) -> dict:
        with open(path, "r") as f:
            return json.load(f)

    def save_pickle(self, data: Any, path: pathlib.Path):
        with open(path, "wb") as f:
            pickle.dump(data, f)

    def load_pickle(self, path: pathlib.Path) -> Any:
        with open(path, "rb") as f:
            return pickle.load(f)
