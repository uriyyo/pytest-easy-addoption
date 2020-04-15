from collections import ChainMap
from dataclasses import InitVar, dataclass, field, fields
from typing import TYPE_CHECKING, Any, ClassVar, Dict, Mapping, Optional, Set, Tuple, Type, cast, get_type_hints

from _pytest_easy_addoption import ConfigHolder

from .missing import MISSING
from .option import Option
from .types import TypeOption

SKIP_FIELDS: Set[str] = {"prefix", "config"}

if TYPE_CHECKING:
    from _pytest.config import Config  # pragma: no cover
    from _pytest.config.argparsing import Parser  # pragma: no cover


def _eval_type(type_obj: TypeOption, module: Optional[str], localns: Dict[str, Any]) -> TypeOption:
    if not isinstance(type_obj, str):
        return type_obj

    class _Temp:
        if module:
            __module__ = module

        obj: type_obj  # type: ignore

    return cast(TypeOption, get_type_hints(_Temp, localns=localns)["obj"])


class AddOptionMeta(type):
    def __new__(mcs, name: str, bases: Tuple[Type, ...], namespace: Dict[str, Any]) -> Any:
        prefix: Optional[str] = ChainMap(namespace, *(b.__dict__ for b in bases)).get("prefix")
        module: Optional[str] = namespace.get("__module__")

        for attr, annotation in namespace.get("__annotations__", {}).items():
            if attr not in SKIP_FIELDS:
                namespace[attr] = field(
                    default=Option.from_decl(
                        name=attr,
                        annotation=_eval_type(annotation, module, namespace),
                        prefix=prefix,
                        value=namespace.get(attr, MISSING),
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

        for option in cls.option_fields().values():
            option.register(group)


__all__ = ["AddOption"]
