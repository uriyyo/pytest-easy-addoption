from typing import Any, Callable, Mapping, Optional, Type, TypeVar, Union

from .missing import Missing

T = TypeVar("T")

MappingStrAny = Mapping[str, Any]
TypeOption = Optional[Union[Type, str, Callable, Missing]]
StrOption = Optional[Union[str, Missing]]
BoolOption = Optional[Union[bool, Missing]]

__all__ = ["T", "BoolOption", "MappingStrAny", "TypeOption", "StrOption"]
