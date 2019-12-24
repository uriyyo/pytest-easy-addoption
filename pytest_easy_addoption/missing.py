class Missing:
    __instance__ = None

    def __new__(cls):
        if cls.__instance__ is None:
            cls.__instance__ = super().__new__(cls)

        return cls.__instance__

    def __repr__(self):
        return "Missing()"

    def __bool__(self):
        return False


MISSING = Missing()

__all__ = ["MISSING", "Missing"]
