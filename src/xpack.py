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

from src.type_ import Field_
from . import m


# transfer function type
def asdict_xxxFieldName(field: Field_) -> m.f_value:
    pass

asdict_func_type = asdict_xxxFieldName


def asdict(obj, *, dict_factory=dict):
    if not m.is_dataclass_instance(obj):
        raise TypeError("asdict() should be called on dataclass instances")
    return __asdict_inner(obj, dict_factory)


def __asdict_inner(obj, dict_factory):
    if m.is_dataclass_instance(obj):
        result = []
        for f in m.fields(obj):
            asdict_fn: asdict_func_type = getattr(obj, f"{m.AsditFuncPrefix}_{f.name}", None)
            if asdict_fn:
                value = asdict_fn(obj.fields.get(f.name))
            else:
                value = __asdict_inner(getattr(obj, f.name), dict_factory)
            result.append((f.name, value))
        return dict_factory(result)

    elif isinstance(obj, list):
        return type(obj)(__asdict_inner(v, dict_factory) for v in obj)
    elif isinstance(obj, dict):
        return type(obj)((__asdict_inner(k, dict_factory),
                          __asdict_inner(v, dict_factory))
                         for k, v in obj.items())
    else:
        return copy.deepcopy(obj)


class EXPack:

    # identification
    __ex_pack_field__ = m.EXPackField

    # reduce memory usage
    __slots__ = ['fields', 'ex_debug']

    def __init__(self, *args, **kwargs):
        self.fields: typing.Dict[m.f_name, Field_] = {}
        self.ex_debug = False

    def _set_properties(self, fields: typing.Dict[m.f_name, Field_] = None) -> 'EXPack':
        self.fields = fields
        return self

    def _with_debug(self, debug: bool) -> 'EXPack':
        self.ex_debug = debug
        return self

    @classmethod
    def json_loads(cls, data: str):
        return cls(**json.loads(data))

    def asdict(self) -> typing.Dict:
        return asdict(self)
