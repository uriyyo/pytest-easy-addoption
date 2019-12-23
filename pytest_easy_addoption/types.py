from typing import Any, Callable, Mapping, Optional, Type, Union, TypeVar

T = TypeVar("T")
C = TypeVar("C")

MappingStrAny = Mapping[str, Any]
OptionType = Optional[Union[Type, str, Callable]]

__all__ = ["T", "C", "MappingStrAny", "OptionType"]
