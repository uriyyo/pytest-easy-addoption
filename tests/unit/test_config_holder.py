from typing import TYPE_CHECKING, cast

from pytest import raises

from pytest_easy_addoption.addoption import ConfigHolder

if TYPE_CHECKING:
    from _pytest.config import Config  # pragma: no cover


def test_get_not_inited_config():
    with raises(ValueError):
        ConfigHolder.get_config()


def test_set_config():
    obj = object()
    ConfigHolder.pytest_configure(cast("Config", obj))

    assert ConfigHolder.get_config() is obj

    ConfigHolder.pytest_unconfigure()

    with raises(ValueError):
        ConfigHolder.get_config()
