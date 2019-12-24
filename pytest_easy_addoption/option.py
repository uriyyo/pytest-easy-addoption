from dataclasses import Field, asdict, dataclass, field, fields
from typing import Any, Generic, Iterable, Mapping, Optional, Sequence, Type, Union

from .missing import MISSING, Missing
from .types import C, MappingStrAny, StrOption, T, TypeOption


def _to_option_name(name: str, prefix: Optional[str]) -> str:
    prefix = "--" if prefix is None else f"--{prefix.replace('_', '-')}-"

    return f"{prefix}{name}".replace("_", "-")


def _to_option_dest(name: str, prefix: Optional[str] = None) -> str:
    prefix = f"{prefix}_" if prefix is not None else ""

    return f"{prefix}{name}"


TYPE_TO_ACTION: Mapping[Type, str] = {bool: "store_true"}


@dataclass
class BaseOption(Generic[T]):
    name: Optional[str] = field(metadata={"skip": True})
    short_name: Optional[str] = field(metadata={"skip": True})
    prefix: Optional[str] = field(metadata={"skip": True})
    use_prefix: bool = field(metadata={"skip": True})
    kwargs: MappingStrAny = field(metadata={"skip": True})

    default: Optional[Union[T, Missing]]
    action: StrOption
    dest: StrOption
    help: StrOption
    type: TypeOption
    required: bool

    @property
    def addoption_names(self) -> Iterable[str]:
        if self.short_name is not MISSING:
            yield f"-{self.short_name}"

        yield _to_option_name(self.name, self.prefix)

    @property
    def addoption_fields(self) -> Sequence[Field]:
        return [f for f in fields(self) if not f.metadata.get("skip")]

    @property
    def addoption_kwargs(self) -> Mapping[str, Any]:
        return {
            f.name: getattr(self, f.name)
            for f in self.addoption_fields
            if getattr(self, f.name) is not MISSING
        }


class Option(BaseOption[T]):
    def __init__(
        self,
        default: Optional[Union[T, Missing]] = MISSING,
        *,
        name: StrOption = MISSING,
        short_name: StrOption = MISSING,
        action: StrOption = MISSING,
        dest: StrOption = MISSING,
        help: StrOption = MISSING,
        type: TypeOption = MISSING,
        required: bool = MISSING,
        prefix: Optional[str] = None,
        use_prefix: bool = True,
        **kwargs: Any,
    ):
        # Option isn't required, but no default value provided
        if default is MISSING and required is not MISSING and not required:
            raise ValueError("No default value provided")

        # Default value set and no required pass, assume that this option required
        if default is not MISSING and required is MISSING:
            required = True

        # No destination provided, generate default one
        if dest is MISSING and name is not MISSING:
            dest = _to_option_dest(name, prefix)

        # No action provided, use default for type or "store"
        if action is MISSING:
            action = TYPE_TO_ACTION.get(type, "store")

        super().__init__(
            default=default,
            name=name,
            short_name=short_name,
            action=action,
            dest=dest,
            help=help,
            type=type,
            required=required,
            use_prefix=use_prefix,
            prefix=prefix,
            kwargs=kwargs,
        )

    @classmethod
    def replace(cls, obj: C, **changes) -> C:
        data = asdict(obj)
        kwargs = changes.pop("kwargs", data.pop("kwargs"))

        return cls(**{**changes, **data, **kwargs})

    @classmethod
    def from_decl(
        cls: Type[C],
        name: str,
        prefix: Optional[str],
        annotation: TypeOption,
        value: Union[T, "Option"],
    ) -> C:
        if not isinstance(value, Option):
            return cls(default=value, name=name, type=annotation, prefix=prefix)

        value.type = value.type or annotation
        value.name = value.name or name
        value.prefix = value.prefix or prefix

        return cls.replace(value)

    def resolve(self, config: Any) -> T:
        return config.getoption(self.dest)

    def register(self, group):
        group.addoption(*self.addoption_names, **self.addoption_kwargs, **self.kwargs)


__all__ = ["Option"]
