from typing import TYPE_CHECKING

from pytest import hookimpl

from .config_holder import ConfigHolder

if TYPE_CHECKING:
    from _pytest.config import Config


@hookimpl(tryfirst=True)
def pytest_configure(config: "Config") -> None:
    ConfigHolder.set_config(config)


@hookimpl(trylast=True)
def pytest_unconfigure() -> None:
    ConfigHolder.set_config(None)
