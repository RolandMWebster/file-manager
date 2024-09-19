from __future__ import annotations

from typing import TYPE_CHECKING, Type

from swapstore.file_handlers.azure_handler import AzureHandler
from swapstore.file_handlers.google_handler import GoogleHandler
from swapstore.file_handlers.local_handler import LocalHandler
from swapstore.file_handlers.none_handler import NoneHandler
from swapstore.file_handlers.s3_handler import S3Handler

if TYPE_CHECKING:
    from swapstore.file_handlers.base_handler import BaseHandler

HANDLER_MAP = {
    "local": LocalHandler,
    "azure": AzureHandler,
    "s3": S3Handler,
    "google": GoogleHandler,
    "none": NoneHandler,
}


class UnknownLocationType(Exception):
    pass


def get_handler_type(location_type: str) -> Type[BaseHandler]:
    try:
        return HANDLER_MAP[location_type]
    except KeyError:
        raise UnknownLocationType()
