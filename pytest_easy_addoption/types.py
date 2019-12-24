from typing import Any, Callable, Mapping, Optional, Type, TypeVar, Union

from .missing import Missing

T = TypeVar("T")
C = TypeVar("C")

MappingStrAny = Mapping[str, Any]
TypeOption = Optional[Union[Type, str, Callable, Missing]]
StrOption = Optional[Union[str, Missing]]

__all__ = ["T", "C", "MappingStrAny", "TypeOption", "StrOption"]
