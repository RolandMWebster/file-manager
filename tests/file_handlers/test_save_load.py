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

import pandas as pd
import pytest
from dotenv import load_dotenv

from swapstore.file_handlers import AzureHandler, GoogleHandler, LocalHandler, S3Handler

load_dotenv()


@pytest.fixture(params=["google", "azure", "s3", "local"])
def handler(request):
    map = {
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
    return map[request.param]


@pytest.mark.remote
def test_read_write_csv(example_df, file_path, handler):
    handler.save_csv(example_df, f"{file_path}.csv")
    loaded_df = handler.load_csv(f"{file_path}.csv")
    pd.testing.assert_frame_equal(example_df, loaded_df)


@pytest.mark.remote
def test_read_write_parquet(example_df, file_path, handler):
    handler.save_parquet(example_df, f"{file_path}.parquet")
    loaded_df = handler.load_parquet(f"{file_path}.parquet")
    pd.testing.assert_frame_equal(example_df, loaded_df)


@pytest.mark.remote
def test_read_write_json(example_dict, file_path, handler):
    handler.save_json(example_dict, f"{file_path}.json")
    loaded_dict = handler.load_json(f"{file_path}.json")
    assert example_dict == loaded_dict


@pytest.mark.remote
def test_read_write_pkl(example_class, file_path, handler):
    handler.save_pickle(example_class, f"{file_path}.pkl")
    loaded_class = handler.load_pickle(f"{file_path}.pkl")
    assert example_class == loaded_class
