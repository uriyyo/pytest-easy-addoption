from typing import TYPE_CHECKING

from pytest import hookimpl

from pkg_resources import iter_entry_points

from .config_holder import ConfigHolder

if TYPE_CHECKING:
    from _pytest.config import Config
    from _pytest.config.argparsing import Parser


def pytest_addoption(parser: "Parser") -> None:
    for entry in iter_entry_points(group="pytest-easy-addoption"):
        cls = entry.resolve()
        cls.register(parser)


@hookimpl(tryfirst=True)
def pytest_configure(config: "Config") -> None:
    ConfigHolder.set_config(config)


@hookimpl(trylast=True)
def pytest_unconfigure() -> None:
    ConfigHolder.set_config(None)
