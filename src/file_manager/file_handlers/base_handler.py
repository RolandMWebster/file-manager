import pathlib
from abc import ABC, abstractmethod
from typing import Any

import pandas as pd


class BaseHandler(ABC):
    """
    Abstract base class for file handlers. This class defines the interface for file
    handlers. All file handlers should inherit from this class and implement the
    methods defined here.
    """

    def __init__(self):
        pass

    def save(self, data: Any, path: pathlib.Path):
        """
        Saves data to a file.

        Parameters
        ----------
        data : Any
            The data to be saved.

        path : pathlib.Path
            The path to save the data to.
        """
        if isinstance(data, pd.DataFrame):
            # check if extension is csv
            if path.suffix == ".csv":
                self.save_csv(data, path)
            elif path.suffix == ".parquet":
                self.save_parquet(data, path)
            else:
                raise NotImplementedError
        elif isinstance(data, dict):
            if path.suffix == ".json":
                self.save_json(data, path)
            else:
                raise NotImplementedError
        else:
            raise NotImplementedError

    def load(self, path: pathlib.Path) -> Any:
        """
        Loads data from a file.

        Parameters
        ----------
        path : pathlib.Path
            The path to the file to load.

        Returns
        -------
        Any
            The loaded data.
        """
        if path.suffix == ".csv":
            return self.load_csv(path)
        elif path.suffix == ".parquet":
            return self.load_parquet(path)
        elif path.suffix == ".json":
            return self.load_json(path)
        else:
            raise NotImplementedError

    @abstractmethod
    def save_csv(self, data: pd.DataFrame, path: pathlib.Path):
        """
        Saves a pandas dataframe to a CSV file.

        Parameters
        ----------
        data : pd.DataFrame
            The data to be saved.

        path : pathlib.Path
            The path to save the data to.
        """
        raise NotImplementedError

    @abstractmethod
    def load_csv(self, path: pathlib.Path) -> pd.DataFrame:
        """
        Loads a CSV file into a pandas dataframe.

        Parameters
        ----------
        path : pathlib.Path
            The path to the CSV file.
        """
        raise NotImplementedError

    @abstractmethod
    def save_parquet(self, data: pd.DataFrame, path: pathlib.Path):
        """
        Saves a pandas dataframe to a parquet file.

        Parameters
        ----------
        data : pd.DataFrame
            The data to be saved.

        path : pathlib.Path
            The path to save the data to.
        """
        raise NotImplementedError

    @abstractmethod
    def load_parquet(self, path: pathlib.Path) -> pd.DataFrame:
        """
        Loads a parquet file into a pandas dataframe.

        Parameters
        ----------
        path : pathlib.Path
            The path to the parquet file.
        """
        raise NotImplementedError

    @abstractmethod
    def save_json(self, data: dict, path: pathlib.Path):
        """
        Saves a dictionary to a JSON file.

        Parameters
        ----------
        data : dict
            The data to be saved.
        path : pathlib.Path
            The path to save the data to.
        """
        raise NotImplementedError

    @abstractmethod
    def load_json(self, path: pathlib.Path) -> dict:
        """
        Loads a JSON file into a dictionary.

        Parameters
        ----------
        path : pathlib.Path
            The path to the JSON file.
        """
        raise NotImplementedError

    @abstractmethod
    def save_pickle(self, data: Any, path: pathlib.Path):
        """
        Saves data to a pickle file.

        Parameters
        ----------
        data : Any
            The data to be saved.
        path : pathlib.Path
            The path to save the data to.
        """
        raise NotImplementedError

    @abstractmethod
    def load_pickle(self, path: pathlib.Path) -> Any:
        """
        Loads a pickle file into a Python object.

        Parameters
        ----------
        path : pathlib.Path
            The path to the pickle file.
        """
        raise NotImplementedError
