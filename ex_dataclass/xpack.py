"""
Ex Dataclass X-Pack

The extend tools for ex_dataclass
1. json loads
2. asdict
3. argument signature
"""
import copy
import json
import typing

from ex_dataclass.type_ import Field_
from . import m


def asdict(obj, *, dict_factory=dict):
    if not m.is_dataclass_instance(obj):
        raise TypeError("asdict() should be called on ex_dataclass instances")
    return __asdict_inner(obj, dict_factory)


def __asdict_inner(obj, dict_factory):
    if m.is_dataclass_instance(obj):
        result = []
        for f in m.fields(obj):
            dict_filed_name = f.label if f.label else f.name
            if m.is_expack(obj):
                asdict_fn: m.asdict_func_type = getattr(obj, f"{m.AsdictFuncPrefix}_{f.name}", None)
                if asdict_fn:
                    result.append(
                            (dict_filed_name, asdict_fn(getattr(obj, f.name, None)))
                    )

                    continue
                # fields_xx 存在于 expack
                if hasattr(obj, "fields_xx"):
                    filed_obj = obj.fields_xx.get(f.name, None)
                    if filed_obj:
                        if filed_obj.outside_field.asdict_factory:
                            result.append(
                                    (dict_filed_name,
                                     filed_obj.outside_field.asdict_factory(getattr(obj, f.name, None)))
                            )
                            continue

            value = __asdict_inner(getattr(obj, f.name), dict_factory)
            result.append((dict_filed_name, value))
        return dict_factory(result)

    elif isinstance(obj, list):
        return type(obj)(__asdict_inner(v, dict_factory) for v in obj)
    elif isinstance(obj, dict):
        return type(obj)((__asdict_inner(k, dict_factory),
                          __asdict_inner(v, dict_factory))
                         for k, v in obj.items())
    else:
        return copy.deepcopy(obj)


class EXpack:
    # identification
    __ex_pack_field__ = m.EXPackField

    # reduce memory usage
    __slots__ = ['__fields_xx', '__ex_debug_xx']

    def __init__(self, *args, **kwargs):
        self.__fields_xx: typing.Dict[m.F_NAME, Field_] = {}
        self.__ex_debug_xx = False

    @property
    def fields_xx(self) -> typing.Dict[m.F_NAME, Field_]:
        return self.__fields_xx

    def _set_properties(self, fields: typing.Dict[m.F_NAME, Field_] = None) -> 'EXpack':
        self.__fields_xx = fields
        return self

    def _with_debug(self, debug: bool) -> 'EXpack':
        self.__ex_debug_xx = debug
        return self

    def asdict(self) -> typing.Dict:
        return asdict(self)

    @classmethod
    def json_loads(cls, data: str):
        return cls(**json.loads(data))

    def json_dumps(self) -> str:
        return json.dumps(asdict(self))

    def pprint(self):
        import pprint
        pprint.pprint(asdict(self))
