import pytest

from file_manager.exceptions import UnknownLocationType
from file_manager.file_handlers import LocalHandler, get_handler


def test_bad_location_type():
    with pytest.raises(UnknownLocationType):
        get_handler(location_type="")


def test_working_location_type():
    handler = get_handler(location_type="local")
    assert handler == LocalHandler
