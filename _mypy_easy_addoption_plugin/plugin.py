from typing import Callable, Optional, Type

from mypy.nodes import AssignmentStmt, TempNode
from mypy.plugin import ClassDefContext, Plugin


def addoption_class_callback(context: ClassDefContext) -> None:
    for stmt in context.cls.defs.body:
        if isinstance(stmt, AssignmentStmt) and stmt.type is not None:
            stmt.rvalue = TempNode(stmt.type, context=stmt.rvalue)


class EasyAddOptionMyPyPlugin(Plugin):
    def get_base_class_hook(self, fullname: str) -> Optional[Callable[[ClassDefContext], None]]:
        if fullname == "easy_addoption.addoption.AddOption":
            return addoption_class_callback

        return None


def plugin(version: str) -> Type[EasyAddOptionMyPyPlugin]:
    return EasyAddOptionMyPyPlugin


__all__ = ["plugin"]
