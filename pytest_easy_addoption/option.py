from typing import Any, Generic, Mapping, Optional, Type, Union

from dataclasses import asdict, dataclass, MISSING

from .types import C, MappingStrAny, OptionType, T


def _default_name(name: str, prefix: Optional[str] = None) -> str:
    prefix = "--" if prefix is None else f"--{prefix}-"

    return f"{prefix}{name}".replace("_", "-")


def _default_dest(name: str, prefix: Optional[str] = None) -> str:
    prefix = f"{prefix}_" if prefix is not None else ""

    return f"{prefix}{name}"


TYPE_TO_ACTION: Mapping[Type, str] = {bool: "store_true"}


@dataclass
class BaseOption(Generic[T]):
    default: Optional[T]
    name: Optional[str]
    short_name: Optional[str]
    action: Optional[str]
    dest: Optional[str]
    help: Optional[str]
    type: OptionType
    required: bool
    prefix: Optional[str]
    use_prefix: bool
    kwargs: MappingStrAny


class Option(BaseOption[T]):
    def __init__(
        self,
        default: Optional[T] = MISSING,
        *,
        name: Optional[str] = None,
        short_name: Optional[str] = None,
        action: Optional[str] = None,
        dest: Optional[str] = None,
        help: Optional[str] = None,
        type: OptionType = None,
        required: bool = MISSING,
        prefix: Optional[str] = None,
        use_prefix: bool = True,
        **kwargs: Any,
    ):
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
    def from_decl(
        cls: Type[C],
        name: str,
        prefix: str,
        annotation: OptionType,
        value: Union[T, "Option"],
    ) -> C:
        if not isinstance(value, Option):
            value = cls(
                default=value, name=_default_name(name, prefix), type=annotation,
            )

        data = asdict(value)
        kwargs = data.pop("kwargs")

        return cls(
            **{
                **data,
                **kwargs,
                "name": value.name
                or _default_name(name, prefix if value.use_prefix else None),
                "dest": value.dest or _default_dest(name, prefix),
                "type": value.type or annotation,
            }
        )

    def resolve(self, config: Any) -> T:
        return config.getoption(self.dest)

    def register(self, group):
        # FIXME: Looks ugly, create one place to configure AddOptions
        fields = {
            key: getattr(self, key)
            for key in ("default", "dest", "help", "type", "required")
        }

        if fields["default"] is not MISSING and fields["required"] is MISSING:
            fields["required"] = False

        group.addoption(
            *((self.short_name,) if self.short_name else ()),
            self.name,
            action=self.action or TYPE_TO_ACTION.get(self.type, "store"),
            **{
                key: value
                for key, value in fields.items()
                if value not in (None, MISSING)
            },
            **self.kwargs,
        )


__all__ = ["Option"]
