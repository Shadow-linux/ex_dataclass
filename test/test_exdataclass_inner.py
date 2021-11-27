import json
import typing

from ex_dataclass import FieldRequiredError
from ex_dataclass.ex_dataclass import ex_dataclass, asdict, field, Field_, EXpack

print("=" * 50 + " basic " + "=" * 50)

name = str
age = int


@ex_dataclass(ex_debug=False)
class ExampleA:
    """
    test type: int, str, float, list, dict, typing.List, typing.Dict
    """
    int_: int = field(default_factory=int)
    str_: str = field(default_factory=str)
    float_: float = field(default_factory=float)
    bool_: bool = field(default_factory=bool)
    list_: list = field(default_factory=list)
    dict_: dict = field(default_factory=dict)
    t_list_1: typing.List[str] = field(default_factory=list)
    t_list_2: typing.List = field(default_factory=list)
    t_dict: typing.Dict[name, age] = field(default_factory=dict)


example_a = ExampleA(**{
    "int_"    : 1,
    "str_"    : "1",
    "float_"  : 0.1,
    "bool_"   : True,
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
class ExBasicB(ExBasicA, EXpack):
    b_1: str = field(default_factory=str)


d = {
    "a_0_1": 2,
    "b_1"  : "b1",
    "a_1"  : "a1",
    "a_2"  : "a2",
}
d_str = json.dumps(d)
ex_basic_b = ExBasicB(**d)
print(ex_basic_b)
assert ex_basic_b.a_1 == "a1", True
print(ex_basic_b.asdict())

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
class ExTypeC(EXpack):
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
print(ex_type_c.asdict())

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
    tl1: typing.List[ExGenericBasic] = field(default_factory=list)


ettwt = ExampleTTypeWithTList(**{
    "tl": [{
        "a1"   : 1,
        "basic": "a"
    }]
})
ettwt1 = ExampleTTypeWithTList(**{
    "tl1": [
        ExGenericA(**{
            "a1"   : 1,
            "basic": "a"
        })
    ]
})
ettwt2 = ExampleTTypeWithTList(**{
    "tl": [
        ExGenericA(**{
            "a1"   : 1,
            "basic": "a"
        })
    ]
})
print(ettwt)
assert type(ettwt.tl[0]) == ExGenericA, True
assert type(ettwt1.tl1[0]) == ExGenericA, True
assert type(ettwt2.tl[0]) == ExGenericA, True

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
        },
        {
            "a2": 1,
            "aa": 2,
        }
    ],
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
class ExampleTListRecursive(EXpack):
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
class ExampleWithMetaClass(EXpack):
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
    "eba"     : ExBasicA(),

}
ewmc = ExampleWithMetaClass(**data)
print(ewmc)
print(ewmc.asdict())

print()
print("=" * 50 + " with EXPack asdict extend functional " + "=" * 50)
import datetime


class NormalClass:

    def __init__(self, user_id: int, username: str):
        self.user_id = user_id
        self.username = username


@ex_dataclass(ex_debug=True)
class ExampleDatetime(EXpack):
    dd: datetime.datetime = field(default=datetime.datetime.now())
    a1: int = field(default_factory=int)
    # normal class
    nc: NormalClass = field(default_factory=dict)
    nc_list: typing.List[NormalClass] = field(default_factory=list)

    def asdict_dd(self, value: datetime.datetime) -> object:
        # print(field.field_name, field.field_value, field.field_type, field.type_name)
        return value.strftime("%Y-%m-%d")

    def asdict_nc(self, value: NormalClass) -> object:
        return {"user_id": value.user_id, "username": value.username}


ed = ExampleDatetime(**{
    "dd"     : datetime.datetime.now(),
    "a1"     : 1,
    "nc"     : NormalClass(user_id=1, username='lisi'),
    "nc_list": [NormalClass(user_id=1, username='lisi')],
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


@ex_dataclass(ex_debug=True)
class TypingUnionNestTypingType(EXpack):
    # expect UnionA
    test1: typing.Union[UnionA, typing.Type[TypeType]] = field(default_factory=UnionA)
    # expect TypeA
    test2: typing.Union[typing.Type[TypeType], UnionA] = field(default_factory=TypeA)
    # expect TypeB
    test3: typing.Union[TypeA, TypeType, TypeB, UnionA] = field(default_factory=TypeB)
    # expect TypeA,TypeB
    test4: typing.List[typing.Union[typing.Type[TypeType], UnionA]] = field(default_factory=list)


data = {
    "test1": UnionA(**{"a1": 1, "a2": 2}),
    "test2": {"a1": 1, "a2": 2, "t1": 1},
    "test3": {"b1": 1, "b2": 2, "t1": 1},
    "test4": [{"a1": 1, "a2": 2, "t1": 1}, {"b1": 1, "b2": 2, "t1": 1}]
}
tuntt = TypingUnionNestTypingType(**data)
print(tuntt)
assert type(tuntt.test1) == UnionA, True
assert type(tuntt.test2) == TypeA, True
assert type(tuntt.test3) == TypeB, True
assert type(tuntt.test4[0]) == TypeA, True
assert type(tuntt.test4[1]) == TypeB, True

print(dir(tuntt))

print()
print("=" * 50 + " field params " + "=" * 50)


@ex_dataclass
class TestFieldParams:
    t_required: str = field(default_factory=str, required=True)


@ex_dataclass
class TestFieldParams1(EXpack):
    t_required: str = field(default_factory=str, required=False)


data = {}
try:
    TestFieldParams(**data)
except FieldRequiredError as e:
    print(e)

data = {
    "t_required": "1"
}
tfp = TestFieldParams1(**data)
print(tfp)
assert tfp.t_required == "1", True

print()
print("=" * 50 + " with EXPack loads extend functional " + "=" * 50)


@ex_dataclass(ex_debug=True)
class WithEXpackLoadsFn(EXpack):
    data: str = field(default_factory=str)

    def loads_data(self, v: int) -> str:
        return str(v)

    def asdict_data(self, v: str) -> int:
        return int(v)


lfn = WithEXpackLoadsFn(**{"data": 1})
print(lfn)
assert isinstance(lfn.data, str), True
data = lfn.asdict()
print(data)
assert isinstance(data['data'], int), True
assert lfn.data == str(1), True

print()
print("=" * 50 + " with dataclass object " + "=" * 50)


@ex_dataclass
class WithExDataClassObject:
    dd: WithEXpackLoadsFn = field(default_factory=WithEXpackLoadsFn)


wedco = WithExDataClassObject(**{"dd": WithEXpackLoadsFn(**{"data": 1})})
print(wedco)
assert wedco.dd.data == "1", True

print()
print("=" * 50 + " with typing ForwardRef (Beta)" + "=" * 50)

hh = str


@ex_dataclass(ex_debug=False)
class AppArgs:
    name: str = field(default="app")
    alias: str = field(default_factory=str)
    help: hh = field(default="add help")
    args: typing.List[typing.List] = field(default_factory=list)
    children: typing.List['AppArgs'] = field(default_factory=list)


dd = {
    "name"    : "xxx",
    "alias"   : "xxx",
    "help"    : 'xxx',
    "args"    : [],
    "children": [
        {
            "name"    : "xxx",
            "alias"   : "xxx",
            "help"    : 'xxx',
            "args"    : [],
            "children": [
                {
                    "name"    : "xxx",
                    "alias"   : "xxx",
                    "help"    : 'xxx',
                    "args"    : [],
                    "children": [

                    ]
                }
            ]
        }
    ]
}

aa = AppArgs(**dd)
print(aa)
assert aa.children[0].children[0].name == "xxx", True


print()
print("=" * 50 + " with EXpack inherit" + "=" * 50)


@ex_dataclass(ex_debug=True)
class WithEXpackBasic(EXpack):

    a1: int = field(default_factory=int)


@ex_dataclass(ex_debug=True)
class WithEXpackInherit(WithEXpackBasic):
    a2: int = field(default_factory=int)


wei = WithEXpackInherit(**{"a1": 10, "a2": 2})
print(wei)
print(wei.fields_xx.get("a1").is_dataclass)