import pathlib
from typing import Any

import pandas as pd

from swapstore.file_handlers.base_handler import BaseHandler


class NoneHandler(BaseHandler):
    """
    None Handler

    This class is a dummy class that does not save or load any data. It is used
    as a placeholder when no file handler is needed. This class is useful for
    testing purposes. For load operations, this class will return an empty object
    of the appropriate type. For save operations, this class will do nothing.

    Examples
    --------
    >>> from file_manager.file_handlers import NoneHandler
    >>> # setup a None handler
    >>> none_handler = NoneHandler()
    """

    def save_csv(self, data: pd.DataFrame, path: pathlib.Path):
        pass

    def load_csv(self, path: pathlib.Path):
        return pd.DataFrame({})

    def save_parquet(self, data: pd.DataFrame, path: pathlib.Path):
        pass

    def load_parquet(self, path: pathlib.Path):
        return pd.DataFrame({})

    def save_json(self, data: dict, path: pathlib.Path):
        pass

    def load_json(self, path: pathlib.Path):
        return {}

    def save_pickle(self, data: Any, path: pathlib.Path):
        pass

    def load_pickle(self, path: pathlib.Path):
        return None
