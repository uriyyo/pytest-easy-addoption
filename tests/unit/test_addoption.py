from dataclasses import is_dataclass

from easy_addoption import AddOption


def test_addoption_is_dataclass():
    class FooAddOption(AddOption):
        pass

    assert is_dataclass(FooAddOption)
