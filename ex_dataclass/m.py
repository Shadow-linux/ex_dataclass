"""
model & utils
"""
import typing
from dataclasses import *

# field type
F_NAME = str
F_TYPE = type
F_VALUE = typing.Any
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
AsdictFuncPrefix = "asdict"
LoadsFuncPrefix = "loads"


# transfer function type
def asdict_xxxFieldName(value: typing.Any) -> F_VALUE:
    pass


asdict_func_type = asdict_xxxFieldName


def loads_xxxFieldName(value: typing.Any) -> F_VALUE:
    pass


loads_func_type = loads_xxxFieldName


def is_expack(obj) -> bool:
    return hasattr(obj, EXPackField)


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
