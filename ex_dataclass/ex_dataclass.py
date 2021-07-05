"""
ex_dataclass
"""
import json
import threading
import typing
import asyncio
from ex_dataclass import m
from ex_dataclass.m import dataclass
from ex_dataclass.type_ import Field_
from ex_dataclass.core import Core
from ex_dataclass.xpack import EXPack, asdict, asdict_func_type
from ex_dataclass.ex_field import field, get_field_witch_cls, check_field_is_required
from ex_dataclass.error import FieldRequiredError

__all__ = [
    'field',
    'asdict',
    'typing',
    'ex_dataclass',
    'asdict_func_type',
    'EXPack',
    'Field_',
    'FieldRequiredError',
]

EX_DEBUG = "ex_debug"

EX_DATACLASS_PARAMS = [
    EX_DEBUG,
]


def __process_e_class(c_class: typing.Type, **kwargs):
    # ex_dataclass params
    debug = kwargs.get(EX_DEBUG, False)

    # pure dataclass kwargs
    kwas = kwargs.keys()
    for p in EX_DATACLASS_PARAMS:
        if p in kwas:
            kwargs.pop(p)

    e_class: typing.Type = dataclass(c_class, **kwargs)
    o_init = e_class.__init__

    def __init__(self, *args, **kwargs):

        # finally kwargs
        nv_kwargs = {}
        props_map = {}
        kwargs_fname_list: typing.List[m.F_NAME] = kwargs.keys()

        # check field required params
        for f_name, ex_field in getattr(e_class, '__dataclass_fields__').items():
            check_field_is_required(e_class.__name__, ex_field, kwargs_fname_list)

        for field_name, field_value in kwargs.items():
            # find field type
            field_type = e_class.__annotations__.get(field_name, None)

            f_ = Field_(e_class=e_class,
                        field_name=field_name,
                        field_value=field_value,
                        field_type=field_type,
                        o_field=get_field_witch_cls(e_class, field_name)
                        )
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


# main
def ex_dataclass(_cls=None, *, ex_debug=False, init=True, repr=True, eq=True, order=False,
                 unsafe_hash=False, frozen=False):
    def wrapper(c_class: typing.Type):
        return __process_e_class(c_class,
                                 ex_debug=ex_debug,
                                 init=init,
                                 repr=repr,
                                 eq=eq,
                                 order=order,
                                 unsafe_hash=unsafe_hash, frozen=frozen)

    if _cls is None:
        return wrapper

    return wrapper(_cls)
