from dataclasses import is_dataclass

from pytest_easy_addoption import AddOption


def test_addoption_is_dataclass():
    class FooAddOption(AddOption):
        pass

    assert is_dataclass(FooAddOption)
