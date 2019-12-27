from pytest import mark, raises

from easy_addoption import Option
from easy_addoption.exceptions import InvalidOptionException


@mark.parametrize(
    "kwargs,expected",
    [
        ({"name": "name"}, ["--name"]),
        ({"short_name": "n"}, ["-n"]),
        ({"name": "name", "short_name": "n"}, ["-n", "--name"]),
    ],
    ids=["only-name", "only-short-name", "name-and-short-name"],
)
def test_names(kwargs, expected):
    option = Option(**kwargs)
    assert [*option.addoption_names] == expected


def test_required_without_default():
    with raises(ValueError):
        Option(required=True)


def test_addoption_fields():
    option = Option()

    assert {f.name for f in option.addoption_fields} == {"default", "action", "dest", "help", "type", "required"}


@mark.parametrize(
    "kwargs,expected",
    [
        ({"default": None}, {"default": None, "action": "store", "required": False}),
        ({"default": None, "type": bool}, {"default": None, "action": "store_true", "required": False, "type": bool}),
        ({"default": None, "name": "name"}, {"default": None, "action": "store", "required": False, "dest": "name"},),
        ({"required": False, "dest": "my_dest"}, {"action": "store", "required": False, "dest": "my_dest"}),
        (
            {"required": False, "name": "dest", "prefix": "my"},
            {"action": "store", "required": False, "dest": "my_dest"},
        ),
        ({"required": False}, {"action": "store", "required": False}),
    ],
    ids=["default-none", "type-bool", "with-name", "with-dest", "with-name-and-prefix", "no-default"],
)
def test_addoption_kwargs(kwargs, expected):
    option = Option(**kwargs)

    assert option.addoption_kwargs == expected


@mark.parametrize(
    "kwargs", [{"default": None}, {"default": None, "short_name": "n"}], ids=["no-names", "no-name-and-dest"]
)
def test_check_ready(kwargs):
    with raises(InvalidOptionException):
        Option(**kwargs).check_ready()


def test_replace():
    option = Option(None)
    obj = object()

    option = option.replace(option, default=obj)
    assert option.default is obj
