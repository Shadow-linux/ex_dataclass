import json
import typing
from ex_dataclass import ex_dataclass, asdict, field
from src.type_ import Field_
from src.xpack import EXPack

print("=" * 50 + " basic " + "=" * 50)


@ex_dataclass(ex_debug=False)
class ExampleA:
    """
    test type: int, str, float, list, dict, typing.List, typing.Dict
    """
    int_: int = field(default_factory=int)
    str_: str = field(default_factory=str)
    float_: float = field(default_factory=float)
    list_: list = field(default_factory=list)
    dict_: dict = field(default_factory=dict)
    t_list_1: typing.List[str] = field(default_factory=list)
    t_list_2: typing.List = field(default_factory=list)
    # t_dict: typing.Dict = field(default_factory=dict)


example_a = ExampleA(**{
    "int_"    : 1,
    "str_"    : "1",
    "float_"  : 0.1,
    "list_"   : [1, 2],
    "dict_"   : {"a": 1, "b": 2},
    "t_list_1": ["1", "2", "3"],
    "t_list_2": ["1", "2", "3"],
    "t_dict"  : {"a": 1, "b": 2}
})
print(example_a)
assert example_a.dict_ == {"a": 1, "b": 2}, True
print(asdict(example_a))

print()
print("=" * 50 + " inherit " + "=" * 50)


@ex_dataclass
class ExBasicA0:
    a_0_1: int = field(default_factory=int)


@ex_dataclass
class ExBasicA(ExBasicA0):
    a_1: str = field(default_factory=str)
    a_2: int = field(default_factory=str)


@ex_dataclass
class ExBasicB(ExBasicA):
    b_1: str = field(default_factory=str)


d = {
    "a_0_1": 1,
    "b_1"  : "b1",
    "a_1"  : "a1",
    "a_2"  : "a2",
}
d_str = json.dumps(d)
ex_basic_b = ExBasicB(**d)
print(ex_basic_b)
assert ex_basic_b.a_1 == "a1", True
print(asdict(ex_basic_b))

print()
print("=" * 50 + " custom type " + "=" * 50)


@ex_dataclass
class ExTypeA:
    a1: str = field(default_factory=str)
    a2: str = field(default_factory=str)


@ex_dataclass
class ExTypeB:
    b1: int = field(default_factory=int)
    b2: int = field(default_factory=int)


@ex_dataclass(ex_debug=True)
class ExTypeC:
    c_a: ExTypeA = field(default_factory=ExTypeA)
    c_b: ExTypeB = field(default_factory=ExTypeB)
    c_list_a: typing.List[ExTypeA] = field(default_factory=list)
    c_list_b: typing.List[ExTypeB] = field(default_factory=list)
    c_list_c: typing.List[ExBasicB] = field(default_factory=list)


ex_type_c = ExTypeC(**{
    "c_a"     : {
        "a1": "1",
        "a2": "2"
    },
    "c_b"     : {
        "b1": 1,
        "b2": 2,
    },
    "c_list_a": [
        {
            "a1": "1",
            "a2": "2"
        },
        {
            "a1": "3",
            "a2": "4"
        }
    ],
    "c_list_b": [
        {
            "b1": 1,
            "b2": 2,
        }
    ],
    "c_list_c": [
        {
            "a_0_1": 1,
            "b_1"  : "b1",
            "a_1"  : "a1",
            "a_2"  : "a2",
        }
    ]
})

print(ex_type_c)
print(ex_type_c.c_list_a[0])
print(ex_type_c.c_list_b[0])
assert ex_type_c.c_a.a1 == "1", True
assert ex_type_c.c_b.b1 == 1, True
assert ex_type_c.c_list_a[0].a1 == "1", True
assert type(ex_type_c.c_list_c[0]) == ExBasicB, True

print()
# 多类型下自动选择最优解，优先级从左到右
print("=" * 50 + " typing union  " + "=" * 50)


@ex_dataclass
class ExUnionTA_1:
    a1: int = field(default_factory=int)
    aa: int = field(default_factory=int)


@ex_dataclass
class ExUnionTA_2:
    a2: int = field(default_factory=int)
    aa: int = field(default_factory=int)


@ex_dataclass
class ExUnionTA_2_1:
    a2: int = field(default_factory=int)
    # type is difference
    aa: str = field(default_factory=str)


@ex_dataclass(ex_debug=True)
class ExampleUnion:
    u1: int = field(default_factory=int)
    # test typing.Union, expect ExUnionTA_1
    u2: typing.Union[ExUnionTA_1, ExUnionTA_2, ExUnionTA_2_1] = field(default_factory=ExUnionTA_1)
    # test typing.Union, expect ExUnionTA_2
    u3: typing.Union[ExUnionTA_1, ExUnionTA_2, ExUnionTA_2_1] = field(default_factory=ExUnionTA_2)
    # test typing.Union, expect ExUnionTA_2_1
    u4: typing.Union[ExUnionTA_1, ExUnionTA_2, ExUnionTA_2_1] = field(default_factory=ExUnionTA_2_1)


eu = ExampleUnion(**{
    "u1": 100,
    "u2": {
        "a1": 1,
        "aa": 2,
    },
    "u3": {
        "a2": 1,
        "aa": 2,
    },
    "u4": {
        "a2": 1,
        "aa": "2",
    },
})

print(eu)
assert eu.u1 == 100, True
assert type(eu.u2) == ExUnionTA_1, True
assert type(eu.u3) == ExUnionTA_2, True
assert type(eu.u4) == ExUnionTA_2_1, True

print()
print("=" * 50 + " typing type  " + "=" * 50)


# 泛型下自动选择最优解，计算顺序根据定义顺序
@ex_dataclass
class ExGenericBasic:
    basic: str = field(default_factory=str)


@ex_dataclass
class ExGenericA(ExGenericBasic):
    a1: int = field(default_factory=int)


@ex_dataclass
class ExGenericB(ExGenericBasic):
    b1: int = field(default_factory=int)


@ex_dataclass(ex_debug=False)
class ExampleTypingType:
    tt: str = field(default_factory=str)
    # expect ExGenericA
    g_type_a: typing.Type[ExGenericBasic] = field(default_factory=ExGenericA)
    # expect ExGenericB
    g_type_b: typing.Type[ExGenericBasic] = field(default_factory=ExGenericB)
    # expect ExGenericBasic
    g_type_basic: typing.Type[ExGenericBasic] = field(default_factory=ExGenericBasic)


ett = ExampleTypingType(**{
    "tt"          : "basic",
    "g_type_a"    : {
        "a1"   : 1,
        "basic": "a"
    },
    "g_type_b"    : {
        "b1"   : 1,
        "basic": "b"
    },
    "g_type_basic": {
        "basic": "basic"
    }
})

print(ett)
assert type(ett.g_type_a) == ExGenericA, True
assert type(ett.g_type_b) == ExGenericB, True
assert type(ett.g_type_basic) == ExGenericBasic, True

print()
print("=" * 50 + " typing type with typing list  " + "=" * 50)


@ex_dataclass(ex_debug=False)
class ExampleTTypeWithTList:
    # expect typing.List[ExGenericA]
    tl: typing.List[typing.Type[ExGenericBasic]] = field(default_factory=list)


ettwt = ExampleTTypeWithTList(**{
    "tl": [{
        "a1"   : 1,
        "basic": "a"
    }]
})
ettwt1 = ExampleTTypeWithTList(**{
    "tl": []
})
print(ettwt)
assert type(ettwt.tl[0]) == ExGenericA, True
assert ettwt1.tl == [], True

print()
print("=" * 50 + " typing union with typing list  " + "=" * 50)


@ex_dataclass(ex_debug=False)
class ExampleTUnionWithTList:
    # expect typing.List[ExUnionTA_1]
    tl1: typing.List[typing.Union[ExUnionTA_2, ExUnionTA_1]] = field(default_factory=list)
    # expect typing.List[ExUnionTA_2]
    tl2: typing.List[typing.Union[ExUnionTA_2, ExUnionTA_1]] = field(default_factory=list)


etuwt = ExampleTUnionWithTList(**{
    "tl1": [{
        "a1": 1,
        "aa": 2,
    }],
    "tl2": [{
        "a2": 1,
        "aa": 2,
    }],

})

print(etuwt)
print(asdict(etuwt))
assert type(etuwt.tl1[0]) == ExUnionTA_1, True
assert type(etuwt.tl2[0]) == ExUnionTA_2, True

print()
print("=" * 50 + " typing list recursive " + "=" * 50)


@ex_dataclass(ex_debug=False)
class ExampleTListRecursive(EXPack):
    tl1: typing.List[typing.List[int]] = field(default_factory=list)
    tl2: typing.List[typing.List[typing.List[int]]] = field(default_factory=list)
    tl3: typing.List[typing.List[ExTypeB]] = field(default_factory=list)
    # expect ExGenericB or ExGenericA
    tl4: typing.List[typing.List[typing.Type[ExGenericBasic]]] = field(default_factory=list)
    # expect ExUnionTA_1 or ExUnionTA_2
    tl5: typing.List[typing.List[typing.Union[ExUnionTA_1, ExUnionTA_2]]] = field(default_factory=list)
    tl6: typing.List[typing.List[int]] = field(default_factory=list)


etlr = ExampleTListRecursive(**{
    "tl1": [[1, 2], [3, 4]],
    "tl2": [[[1, 2], [3, 4]]],
    "tl3": [
        [{"b1": 1, "b2": 2}, {"b1": 3, "b2": 4}],
        [{"b1": 5, "b2": 6}, {"b1": 7, "b2": 8}],
    ],
    "tl4": [
        [{"b1": 1, "basic": "b"}, {"b1": 2, "basic": "b"}],
        [{"a1": 1, "basic": "a"}, {"a1": 2, "basic": "a"}]
    ],
    "tl5": [
        [{"a1": 1, "aa": 1}, {"a2": 2, "aa": 2}]
    ],
    "tl6": []
})
print(etlr)
assert etlr.tl2 == [[[1, 2], [3, 4]]], True
assert type(etlr.tl3[0][0]) == ExTypeB, True
assert type(etlr.tl3[1][0]) == ExTypeB, True
assert type(etlr.tl4[0][0]) == ExGenericB, True
assert type(etlr.tl4[1][0]) == ExGenericA, True
assert type(etlr.tl5[0][0]) == ExUnionTA_1, True
assert type(etlr.tl5[0][1]) == ExUnionTA_2, True
assert etlr.tl6 == [], True

print()
print("=" * 50 + " with EXPack " + "=" * 50)


@ex_dataclass(ex_debug=False)
class ExampleWithMetaClass(EXPack):
    """
    test type: int, str, float, list, dict, typing.List, typing.Dict
    """
    int_: int = field(default_factory=int)
    str_: str = field(default_factory=str)
    float_: float = field(default_factory=float)
    list_: list = field(default_factory=list)
    dict_: dict = field(default_factory=dict)
    t_list_1: typing.List[str] = field(default_factory=list)
    t_list_2: typing.List = field(default_factory=list)
    t_dict: typing.Dict = field(default_factory=dict)
    eba: ExBasicA = field(default_factory=ExBasicA)
    asd_test: int = field(default_factory=int)


data = {
    "int_"    : 1,
    "str_"    : "1",
    "float_"  : 0.1,
    "list_"   : [1, 2],
    "dict_"   : {"a": 1, "b": 2},
    "t_list_1": ["1", "2", "3"],
    "t_list_2": ["1", "2", "3"],
    "t_dict"  : {"a": 1, "b": 2},
    "asd_test": 222,

}
data_str = json.dumps(data)
ewmc = ExampleWithMetaClass(**data)
ewmc2 = ExampleWithMetaClass.json_loads(data_str)
print(ewmc)
print(ewmc2)
print(ewmc.asdict())

print()
print("=" * 50 + " with EXPack asdict extend functional " + "=" * 50)
import datetime


class NormalClass:

    def __init__(self, user_id: int, username: str):
        self.user_id = user_id
        self.username = username


@ex_dataclass
class ExampleDatetime(EXPack):
    dd: datetime.datetime = field(default=datetime.datetime.now())
    a1: int = field(default_factory=int)
    # normal class
    nc: NormalClass = field(default_factory=dict)

    def asdict_dd(self, field: Field_) -> object:
        # print(field.field_name, field.field_value, field.field_type, field.type_name)
        return field.field_value.strftime("%Y-%m-%d")

    def asdict_nc(self, field: Field_) -> object:
        nc: NormalClass = field.field_value
        return {"user_id": nc.user_id, "username": nc.username}


ed = ExampleDatetime(**{
    "dd": datetime.datetime.now(),
    "a1": 1,
    "nc": NormalClass(user_id=1, username='lisi'),
})
print(ed)
assert ed.a1 == 1, True
assert type(ed.dd) == datetime.datetime, True
assert ed.nc.user_id == 1, True
ed_dict = ed.asdict()
print(ed_dict)
assert type(ed_dict['dd']) == str, True

print()
print("=" * 50 + " typing type nest typing union " + "=" * 50)


@ex_dataclass()
class UnionA:
    a1: int = field(default_factory=int)
    a2: int = field(default_factory=int)


@ex_dataclass
class TypeType:
    t1: int = field(default_factory=int)


@ex_dataclass
class TypeA(TypeType):
    a1: int = field(default_factory=int)
    a2: int = field(default_factory=int)


@ex_dataclass
class TypeB(TypeType):
    b1: int = field(default_factory=int)
    b2: int = field(default_factory=int)


@ex_dataclass(ex_debug=False)
class TypingUnionNestTypingType(EXPack):
    # expect UnionA
    test1: typing.Union[UnionA, typing.Type[TypeType]] = field(default_factory=UnionA)
    # expect TypeA
    test2: typing.Union[typing.Type[TypeType], UnionA] = field(default_factory=TypeA)
    # expect TypeB
    test3: typing.Union[TypeA, TypeType, TypeB, UnionA] = field(default_factory=TypeB)


data = {
    "test1": {"a1": 1, "a2": 2},
    "test2": {"a1": 1, "a2": 2, "t1": 1},
    "test3": {"b1": 1, "b2": 2, "t1": 1},
}
tuntt = TypingUnionNestTypingType.dict_loads(data)
print(tuntt)
