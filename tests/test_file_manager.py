import os

import pandas as pd
import pytest

from file_manager import FileManager


def test_bad_assignments():
    # no handler or location type supplied
    with pytest.raises(AttributeError):
        FileManager()


@pytest.fixture
def example_df():
    return pd.DataFrame({"col1": [1, 2, 3]})


@pytest.fixture()
def example_dict():
    return {"a": [1, 2, 3], "b": [4, 5, 6]}


@pytest.fixture(autouse=True)
def cleanup_files():
    yield
    for file in os.listdir("tests/data/"):
        if file == ".gitkeep":
            continue
        os.remove(f"tests/data/{file}")


def test_save_load_dataframe(example_df):
    manager = FileManager(default_directory="tests/data/", location_type="local")
    manager.save(example_df, "_test.csv")
    loaded = manager.load("_test.csv")
    assert example_df.equals(loaded)


def test_save_load_json(example_dict):
    manager = FileManager(default_directory="tests/data/", location_type="local")
    manager.save(example_dict, "_test.json")
    loaded = manager.load("_test.json")
    assert example_dict == loaded


def test_save_load_parquet(example_df):
    manager = FileManager(default_directory="tests/data/", location_type="local")
    manager.save(example_df, "_test.parquet")
    loaded = manager.load("_test.parquet")
    assert example_df.equals(loaded)
