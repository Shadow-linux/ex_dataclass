"""
ex_dataclass
"""
import json
import typing
import asyncio
from src import m
from src._turbo import FutureTurboEngine
from src.m import dataclass, field
from src._type import Field_
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
EX_TURBO_ONN = "ex_turbo_on"
EX_CHECK_VALIDATE_TYPE = "ex_check_validate_type"

EX_DATACLASS_PARAMS = [
    EX_DEBUG,
    EX_CHECK_VALIDATE_TYPE,
    EX_TURBO_ONN,
]


def __process_e_class(c_class: typing.Type, **kwargs):
    # ex_dataclass params
    debug = kwargs.get(EX_DEBUG, False)
    turbo_ob = kwargs.get(EX_TURBO_ONN, False)

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
        turbo_engine = None

        if turbo_ob:
            turbo_engine = FutureTurboEngine()

        for field_name, field_value in kwargs.items():
            # find field type
            field_type = e_class.__annotations__.get(field_name, None)

            f_ = Field_(e_class=e_class, field_name=field_name, field_value=field_value, field_type=field_type)
            if debug: print(f_)

            f_.build()
            props_map[field_name] = f_

            # ignore not define property
            if f_.is_abort:
                continue

            Core.DEBUG = debug

            if turbo_engine:
                turbo_engine.refuel(Core.handle, f_)
            else:
                nv_kwargs[field_name] = Core.handle(f_).field_value

        if turbo_engine:
            for f_ in turbo_engine.as_complete():
                nv_kwargs[f_.field_name] = f_.field_value

        o_init(self, *args, **nv_kwargs)
        if getattr(self, m.EXPackField, None):
            self._with_debug(debug)._set_properties(props_map)

    # bind methods
    e_class.__init__ = __init__

    if debug:
        print(f"---- {e_class} ----")

    return e_class

# main
def ex_dataclass(_cls=None, *, ex_debug=False, ex_turbo_on=False, init=True, repr=True, eq=True, order=False,
                 unsafe_hash=False, frozen=False):
    def wrapper(c_class: typing.Type):
        return __process_e_class(c_class,
                                 ex_debug=ex_debug,
                                 ex_turbo_on=ex_turbo_on,
                                 init=init,
                                 repr=repr,
                                 eq=eq,
                                 order=order,
                                 unsafe_hash=unsafe_hash, frozen=frozen)

    if _cls is None:
        return wrapper

    return wrapper(_cls)
