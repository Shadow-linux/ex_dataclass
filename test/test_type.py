import pprint
from dataclasses import dataclass, is_dataclass

from ex_dataclass import ex_dataclass

print(dict.__name__)
print(str.__name__)
print(set.__name__)
print(frozenset.__name__)
print(list.__name__)
print(dict.__dict__)

import typing
from dataclasses import field, asdict, dataclass
# print(typing.List.__dict__.get("_name"))
# print(typing.List.__origin__)
# print(typing.Set[int]._name)
# print()
# print(f"union type: {typing.Union[int, str].__origin__._name}")
# print(typing.Union[int, str].__origin__._name == 'Union')
print(typing.Type[int]._name == 'Type')
print(typing.List[typing.List[int]]._name)




from ex_dataclass import ex_dataclass, asdict, field, EXpack

@ex_dataclass
class ExTypeA:
    a1: str = field(default_factory=str)
    a2: str = field(default_factory=str)


@ex_dataclass
class ExTypeB:
    b1: int = field(default_factory=int)
    b2: int = field(default_factory=int)


@ex_dataclass
class ExTypeC:
    c_a: ExTypeA = field(default_factory=ExTypeA)
    c_b: ExTypeB = field(default_factory=ExTypeB)


ex_type_c = ExTypeC(**{
    "c_a"     : {
        "a1": "1",
        "a2": "2"
    },
    "c_b"     : {
        "b1": 1,
        "b2": 2,
    },
    })
print(ex_type_c)
print(ex_type_c)
print(type(typing.Type.__args__[0].__class__))
print(is_dataclass(typing.Type[ExTypeC].__args__[0]))
print(typing.Union.__class__)
print(type(typing.List.__args__[0]) == typing.TypeVar)
print(typing.List.__args__)




