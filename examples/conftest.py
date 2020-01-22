from typing import List

import pytest

from easy_addoption import AddOption, Append, Count, Option


class MyAddOption(AddOption):
    flag: bool
    required: int
    with_default: str = "value"
    using_option: float = Option(1.0)
    count: int = Count()
    append: List[str] = Append()


def pytest_addoption(parser):
    MyAddOption.register(parser)


@pytest.fixture(scope="session")
def my_addoption():
    return MyAddOption()
