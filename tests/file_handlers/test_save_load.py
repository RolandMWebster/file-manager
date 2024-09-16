"""
Tests the save and load functionalities of file handlers.

This script makes use of various environment variables that should be stored in a .env
file in the root directory of the project. Ensure a .env file exists with the following
variables defined:
- TESTING_GOOGLE_PROJECT
- TESTING_GOOGLE_BUCKET
- TESTING_AZURE_ACCOUNT_URL
- TESTING_AZURE_CONTAINER
- TESTING_S3_BUCKET
- TESTING_PATH_PREFIX
"""

import os
from dataclasses import dataclass

import pandas as pd
import pytest
from dotenv import load_dotenv

from file_manager.file_handlers import (
    AzureHandler,
    GoogleHandler,
    LocalHandler,
    S3Handler,
)

load_dotenv()

handlers = {
    "google": GoogleHandler(
        project=os.getenv("TESTING_GOOGLE_PROJECT"),
        bucket=os.getenv("TESTING_GOOGLE_BUCKET"),
        path_prefix=os.getenv("TESTING_PATH_PREFIX"),
    ),
    "azure": AzureHandler(
        account_url=os.getenv("TESTING_AZURE_ACCOUNT_URL"),
        container=os.getenv("TESTING_AZURE_CONTAINER"),
        path_prefix=os.getenv("TESTING_PATH_PREFIX"),
    ),
    "s3": S3Handler(
        bucket=os.getenv("TESTING_S3_BUCKET"),
        path_prefix=os.getenv("TESTING_PATH_PREFIX"),
    ),
    "local": LocalHandler(),
}


@dataclass
class ExampleClass:
    a: int
    b: str


FILEPATH = "tests/data/test"


# define some objects to read/write
@pytest.fixture
def example_df():
    return pd.DataFrame({"a": [1, 2], "b": ["example1", "example2"]})


@pytest.fixture
def example_dict():
    return {"key": "value"}


@pytest.fixture
def example_class():
    return ExampleClass(a=1, b="example")


@pytest.mark.parametrize("handler_name", handlers.keys())
def test_read_write_csv(handler_name, example_df):
    handler = handlers[handler_name]
    handler.save_csv(example_df, f"{FILEPATH}.csv")
    loaded_df = handler.load_csv(f"{FILEPATH}.csv")
    pd.testing.assert_frame_equal(example_df, loaded_df)


@pytest.mark.parametrize("handler_name", handlers.keys())
def test_read_write_parquet(handler_name, example_df):
    handler = handlers[handler_name]
    handler.save_parquet(example_df, f"{FILEPATH}.parquet")
    loaded_df = handler.load_parquet(f"{FILEPATH}.parquet")
    pd.testing.assert_frame_equal(example_df, loaded_df)


@pytest.mark.parametrize("handler_name", handlers.keys())
def test_read_write_json(handler_name, example_dict):
    handler = handlers[handler_name]
    handler.save_json(example_dict, f"{FILEPATH}.json")
    loaded_dict = handler.load_json(f"{FILEPATH}.json")
    assert example_dict == loaded_dict


@pytest.mark.parametrize("handler_name", handlers.keys())
def test_read_write_pkl(handler_name, example_class):
    handler = handlers[handler_name]
    handler.save_pickle(example_class, f"{FILEPATH}.pkl")
    loaded_class = handler.load_pickle(f"{FILEPATH}.pkl")
    assert example_class == loaded_class
