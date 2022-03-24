"""
ex_dataclass
https://github.com/Shadow-linux/ex_dataclass
"""
import json
import threading
import typing
import logging
import asyncio
from ex_dataclass import m
from ex_dataclass.m import dataclass, asdict_func_type, loads_func_type
from ex_dataclass.type_ import Field_
from ex_dataclass.core import Core
from ex_dataclass.xpack import EXpack, asdict
from ex_dataclass.ex_field import field, get_field_witch_cls, check_field_is_required
from ex_dataclass.error import FieldRequiredError, FieldNotMatchValueError

__all__ = [
    'field',
    'asdict',
    'typing',
    'ex_dataclass',
    'EXpack',
    'Field_',
    'FieldRequiredError',
    'FieldNotMatchValueError',
    'loads_func_type',
    'asdict_func_type',
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

    # label map
    label_2_field_name_map = {}

    e_class: typing.Type = dataclass(c_class, **kwargs)
    o_init = e_class.__init__

    def __init__(self, *args, **kwargs):

        # finally kwargs
        nv_kwargs = {}
        expack_fileds_map = {}
        kwargs_fname_list: typing.List[m.F_NAME] = kwargs.keys()
        print(kwargs)
        # check field required params
        for f_name, ex_field in getattr(e_class, m.DataClassFields).items():
            label_2_field_name_map[ex_field.label] = f_name
            check_field_is_required(e_class.__name__, ex_field, kwargs_fname_list)


        for field_name, field_value in kwargs.items():
            # find field type
            field_type = e_class.__annotations__.get(field_name, None)

            # get the ex_dataclass field name from label_map
            cls_field_name = label_2_field_name_map.get(field_name, field_name)
            ex_field_obj = get_field_witch_cls(e_class, cls_field_name)

            f_ = Field_(e_class=e_class,
                        field_name=cls_field_name,
                        field_value=field_value,
                        field_type=field_type,
                        o_field=ex_field_obj,
                        )
            if debug: print(f_)

            f_.build()
            expack_fileds_map[cls_field_name] = f_

            # is dataclass instance
            if f_.is_dataclass:
                nv_kwargs[cls_field_name] = field_value
            # ignore not define property
            if f_.is_abort:
                if debug: print(f"{f_} will be ignored.")
                continue

            if m.is_expack(self):
                # loads_factory
                if ex_field_obj.loads_factory:
                    nv_kwargs[cls_field_name] = ex_field_obj.loads_factory(field_value)
                    continue

                # loads_<FieldName>
                lfn: m.loads_func_type = getattr(self, f"{m.LoadsFuncPrefix}_{cls_field_name}", None)
                if lfn:
                    if debug: print(f"{f_} loads from {m.LoadsFuncPrefix}_{cls_field_name}.")
                    nv_kwargs[cls_field_name] = lfn(field_value)
                    continue

            Core.DEBUG = debug
            try:
                nv_kwargs[cls_field_name] = Core.handle(f_)
            except TypeError as e:
                logging.exception(e)
                raise FieldNotMatchValueError(filed_name=f_.field_name, field_type=f_.field_type)
            except Exception as e:
                raise e


        o_init(self, *args, **nv_kwargs)
        if m.is_expack(self):
            self._with_debug(debug)._set_properties(expack_fileds_map)

    # bind methods
    e_class.__init__ = __init__

    # 缓存 e_class
    m.E_CLASS_CACHE[e_class.__name__] = e_class

    if debug:
        print(f"---- {e_class.__name__} ----")
        print(f"E_CLASS CACHE: {m.E_CLASS_CACHE}")

    return e_class


# main
def ex_dataclass(_cls=None, *, ex_debug: bool = False, init: bool = True, repr: bool = True, eq: bool = True,
                 order: bool = False,
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
