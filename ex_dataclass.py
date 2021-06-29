"""
ex_dataclass
"""
import json
import typing
from src import m
from src.m import dataclass, field
from src.type_ import Field_
from src.core import Core
from src.xpack import EXPack, asdict, asdict_func_type

__all__ = [
    'field',
    'asdict',
    'typing',
    'ex_dataclass',
    'asdict_func_type',
    'EXPack',
    'Field_'
]

EX_DEBUG = "ex_debug"
EX_CHECK_VALIDATE_TYPE = "ex_check_validate_type"

EX_DATACLASS_PARAMS = [
    EX_DEBUG,
    EX_CHECK_VALIDATE_TYPE
]


def __process_e_class(c_class: typing.Type, *args: typing.Tuple, **kwargs: typing.Dict):
    # ex_dataclass params
    debug = kwargs.get(EX_DEBUG, False)
    check_validate_type = kwargs.get('check_validate_type', False)

    # pure dataclass kwargs
    kwas = kwargs.keys()
    for p in EX_DATACLASS_PARAMS:
        if p in kwas:
            kwargs.pop(p)

    e_class: typing.Type = dataclass(c_class, **kwargs)

    if not hasattr(e_class, '__annotations__'):
        raise Exception(f"{e_class} missing required attribute. Did you forget to define attributes ?")
    o_init = e_class.__init__

    def __init__(self, *args, **kwargs):

        # finally kwargs
        nv_kwargs = {}
        props_map = {}

        for field_name, field_value in kwargs.items():
            # find field type
            field_type = e_class.__annotations__.get(field_name, None)

            f_ = Field_(e_class=e_class, field_name=field_name, field_value=field_value, field_type=field_type)
            if debug: print(f_)

            f_.build()

            # ignore not define property
            if f_.is_abort:
                continue

            Core.DEBUG = debug
            nv_kwargs[field_name] = Core.handle(f_)
            props_map[field_name] = f_

        o_init(self, *args, **nv_kwargs)
        if getattr(self, m.EXPackField, None):
            self._with_debug(debug)._set_properties(props_map)

    # bind methods
    e_class.__init__ = __init__

    if debug:
        print(f"---- {e_class} ----")

    return e_class


def ex_dataclass(*args, **kwargs):
    def wrapper(c_class: typing.Type):
        return __process_e_class(c_class, *args, **kwargs)

    return wrapper(args[0]) if args else wrapper
