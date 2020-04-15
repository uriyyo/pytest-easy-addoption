from dataclasses import is_dataclass

from easy_addoption import AddOption


def test_addoption_is_dataclass():
    class FooAddOption(AddOption):
        pass

    assert is_dataclass(FooAddOption)


TypeAlias = str


def test_addoption_type_as_str():
    class FooAddOption(AddOption):
        bar: "TypeAlias"

    assert FooAddOption.bar.type is str
