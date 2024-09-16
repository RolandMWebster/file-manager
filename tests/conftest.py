from dataclasses import dataclass

import pandas as pd
import pytest


@dataclass
class ExampleClass:
    a: int
    b: str


@pytest.fixture
def file_path():
    return "tests/data/test"


@pytest.fixture
def example_df():
    return pd.DataFrame({"a": [1, 2], "b": ["example1", "example2"]})


@pytest.fixture
def example_dict():
    return {"key": "value"}


@pytest.fixture
def example_class():
    return ExampleClass(a=1, b="example")
