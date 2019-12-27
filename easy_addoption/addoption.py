from collections import ChainMap
from dataclasses import InitVar, dataclass, field, fields
from typing import TYPE_CHECKING, Any, ClassVar, Dict, Mapping, Optional, Set, Tuple, Type

from _pytest_easy_addoption import ConfigHolder

from .missing import MISSING
from .option import Option

SKIP_FIELDS: Set[str] = {"prefix", "config"}

if TYPE_CHECKING:
    from _pytest.config import Config  # pragma: no cover
    from _pytest.config.argparsing import Parser  # pragma: no cover


class AddOptionMeta(type):
    def __new__(mcs, name: str, bases: Tuple[Type, ...], namespace: Dict[str, Any]) -> Any:
        prefix: Optional[str] = ChainMap(namespace, *(b.__dict__ for b in bases)).get("prefix")

        for attr, annotation in namespace.get("__annotations__", {}).items():
            if attr not in SKIP_FIELDS:
                namespace[attr] = field(
                    default=Option.from_decl(
                        name=attr, annotation=annotation, prefix=prefix, value=namespace.get(attr, MISSING),
                    ),
                    init=False,
                )

        cls = super().__new__(mcs, name, bases, namespace)
        return dataclass(cls)


@dataclass
class AddOption(metaclass=AddOptionMeta):
    prefix: ClassVar[Optional[str]]
    config: InitVar["Config"] = None

    def __post_init__(self, config: "Config") -> None:
        config = config or ConfigHolder.get_config()

        for name, option in self.option_fields().items():
            setattr(self, name, option.resolve(config))

    @classmethod
    def option_fields(cls) -> Mapping[str, Option]:
        cls_fields = {f.name: f for f in fields(cls)}
        names = {*cls_fields.keys()} - {f.name for f in fields(AddOption)}

        return {name: cls_fields[name].default for name in names}

    @classmethod
    def register(cls, parser: "Parser") -> None:
        group = parser.getgroup(cls.__name__)

        for _, option in cls.option_fields().items():
            option.register(group)


__all__ = ["AddOption"]
