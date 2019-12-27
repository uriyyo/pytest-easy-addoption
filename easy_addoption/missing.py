from typing import Optional, Type


class Missing:
    __instance__: Optional["Missing"] = None

    def __new__(cls: Type["Missing"]) -> "Missing":
        if cls.__instance__ is None:
            cls.__instance__ = super().__new__(cls)

        return cls.__instance__

    def __repr__(self) -> str:
        return "Missing()"

    def __bool__(self) -> bool:
        return False


MISSING = Missing()

__all__ = ["MISSING", "Missing"]
