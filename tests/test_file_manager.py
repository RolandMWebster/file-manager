import os

import pytest

from file_manager import FileManager


@pytest.fixture(autouse=True)
def cleanup_files():
    yield
    for file in os.listdir("tests/data/"):
        if file == ".gitignore":
            continue
        os.remove(f"tests/data/{file}")


@pytest.fixture
def file_manager():
    return FileManager(default_directory="tests/data/", location_type="local")


def test_bad_assignments():
    # no handler or location type supplied
    with pytest.raises(AttributeError):
        FileManager()


def test_save_load_dataframe(example_df, file_manager):
    file_manager.save(example_df, "_test.csv")
    loaded = file_manager.load("_test.csv")
    assert example_df.equals(loaded)


def test_save_load_json(example_dict, file_manager):
    file_manager.save(example_dict, "_test.json")
    loaded = file_manager.load("_test.json")
    assert example_dict == loaded


def test_save_load_parquet(example_df, file_manager):
    file_manager.save(example_df, "_test.parquet")
    loaded = file_manager.load("_test.parquet")
    assert example_df.equals(loaded)


def test_save_load_pkl(example_class, file_manager):
    file_manager.save(example_class, "_test.pkl")
    loaded = file_manager.load("_test.pkl")
    assert example_class == loaded
