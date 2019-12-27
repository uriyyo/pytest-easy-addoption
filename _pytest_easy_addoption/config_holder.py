from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from _pytest.config import Config


class ConfigHolder:
    _config: Optional["Config"] = None

    @classmethod
    def get_config(cls) -> "Config":
        if cls._config is None:
            raise ValueError("Try to use not inited config")

        return cls._config

    @classmethod
    def set_config(cls, config: Optional["Config"]) -> None:
        cls._config = config


__all__ = [
    "ConfigHolder",
]
