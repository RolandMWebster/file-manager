from __future__ import annotations

import pathlib
from typing import TYPE_CHECKING, Any, Optional, Union

from file_manager.file_handlers import get_handler

if TYPE_CHECKING:
    from file_manager.file_handlers import BaseHandler


class FileManager:
    def __init__(
        self,
        default_directory: Optional[Union[str, pathlib.Path]] = None,
        location_type: Optional[str] = None,
        handler: Optional[BaseHandler] = None,
        handler_kwargs: Optional[dict] = None,
    ):
        self.default_directory = default_directory
        if location_type is None and handler is None:
            raise AttributeError(
                "One of either 'location' or 'handler' must be supplied."
            )
        if location_type is not None and handler is not None:
            raise AttributeError(
                "Only one of either 'location' or 'handler' should be supplied."
            )

        self.location_type = location_type

        if handler is None:
            handler_type = get_handler(location_type=self.location_type)
            if handler_kwargs is None:
                handler_kwargs = {}
            self.handler = handler_type(**handler_kwargs)
        else:
            self.handler = handler

    @property
    def default_directory(self):
        return self._default_directory

    @default_directory.setter
    def default_directory(self, value: Optional[Union[pathlib.Path, str]] = None):
        if value is None:
            self._default_directory = None
            return
        if isinstance(value, str):
            value = pathlib.Path(value)
        self._default_directory = value

    def save(self, data: Any, filename: str, directory: Optional[str] = None):
        """
        Save a file.

        Parameters
        ----------
        data : Any
            The data to save.
        filename : str
            The name of the file to save, with the extension.
        directory : str, optional
            The directory to save the file to. If None, the default directory is used.

        Raises
        ------
        AttributeError
            If no directory is supplied and the default_directory is None.
        ValueError
            If the file extension is not included in the `filename` argument.

        Examples
        --------
        >>> from file_manager import FileManager
        >>> manager = FileManager(location_type="local")
        >>> data = {"a": [1, 2, 3], "b": [4, 5, 6]}
        >>> manager.save(
        ...     data=data, filename="data.json", directory="data/docstring_examples/"
        ... )
        >>> # Use the default directory instead of supplying one manually
        >>> manager.default_directory = "data/docstring_examples/"
        >>> manager.save(data=data, filename="data.json")
        """
        if directory is None:
            directory = self.default_directory

        if directory is None:
            raise AttributeError(
                "No directory supplied and default_directory is None. Supply a "
                "directory within the method call or set a default_directory via "
                "manager.default_directory = dir."
            )
        # construct file path
        filepath = self.default_directory / filename
        # check there is a file extension
        if not filepath.suffix:
            raise ValueError("No file extension provided in the 'filename' argument.")
        self.handler.save(data=data, path=filepath)

    def load(self, filename: str, directory: Optional[str] = None) -> Any:
        """
        Load a file.

        Parameters
        ----------
        filename : str
            The name of the file to load, with the extension.
        directory : str, optional
            The directory to load the file from. If None, the default directory is used.

        Returns
        -------
        Any
            The loaded data.

        Raises
        ------
        AttributeError
            If no directory is supplied and the default_directory is None.
        ValueError
            If the file extension is not included in the `filename` argument.

        Examples
        --------
        >>> from file_manager import FileManager
        >>> manager = FileManager(
        ...     location_type="local", default_directory="data/docstring_examples/"
        ... )
        >>> data = {"a": [1, 2, 3], "b": [4, 5, 6]}
        >>> manager.save(data=data, filename="data.json")
        >>> loaded_data = manager.load(filename="data.json")
        >>> loaded_data
        {'a': [1, 2, 3], 'b': [4, 5, 6]}
        """
        if directory is None:
            directory = self.default_directory

        if directory is None:
            raise AttributeError(
                "No directory supplied and default_directory is None. Supply a "
                "directory within the method call or set a default_directory via "
                "manager.default_directory = dir."
            )
        # construct file path
        filepath = self.default_directory / filename

        # check there is a file extension
        if not filepath.suffix:
            raise ValueError("No file extension provided in the 'filename' argument.")
        return self.handler.load(path=filepath)
