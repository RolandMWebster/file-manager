import pytest

from swapstore.exceptions import UnknownLocationType
from swapstore.file_handlers import LocalHandler, get_handler_type


def test_bad_location_type():
    with pytest.raises(UnknownLocationType):
        get_handler_type(location_type="")


def test_working_location_type():
    handler = get_handler_type(location_type="local")
    assert handler == LocalHandler
