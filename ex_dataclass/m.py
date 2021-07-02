"""
model & utils
"""
import typing
from dataclasses import *


# field type
f_name = str
f_type = type
f_value = typing.Any
DataClassObj = object
DataClassType = type
ContainerValues = typing.Iterator

TypingList = "List"
TypingTuple = "Tuple"
TypingSet = "Set"
TypingDict = "Dict"
TypingType = "Type"
TypingUnion = "Union"

EXPackField = "__ex_pack_field__"
DataClassFields = '__dataclass_fields__'
AsditFuncPrefix = "asdict"

def is_dataclass_instance(obj) -> bool:
    """Returns True if obj is an instance of a dataclass."""
    return hasattr(type(obj), DataClassFields)


class ToolImpl:

    def __init__(self, *args, **kwargs):
        self.debug = False

    @classmethod
    def with_debug(cls, debug: bool, *args, **kwargs):
        c = cls(*args, **kwargs)
        c.debug = debug
        return c
