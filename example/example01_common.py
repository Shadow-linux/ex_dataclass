"""
简单使用示例
"""
import typing
import datetime
from ex_dataclass import ex_dataclass, asdict, field, EXpack


# 示例一
@ex_dataclass
class ExampleA:
    # default_factory: 需要给一个类（可callable的对象）
    str_: str = field(default_factory=str)
    # default: 给定一个默认值
    int_: int = field(default=0)
    bool_: bool = field(default_factory=bool)


data = {
    "str_"  : "1",
    "int_"  : 1,
    "bool_" : True,
    # 冗余字段, 会被舍弃
    "float_": 0.0
}
exp_a = ExampleA(**data)
print(exp_a)
# :return: ExampleA(str_='1', int_=1, bool_=True)
# exp_a.str_   // 为的就是方便的自动补全
# exp_a.bool_



# 示例二，使用ExampleA 作为其字段类型。
@ex_dataclass
class ExampleB:
    a1: ExampleA = field(default_factory=ExampleA)
    a2: ExampleA = field(default_factory=dict)
    a3: ExampleA = field(default=None)


# 通过给定不同的默认值，会影响默认行为，可以看到default_factory 和 default 是不会受 ExampleA 类型注解限制赋值。
exp_b = ExampleB()
print(exp_b)
# :return: ExampleB(a1=ExampleA(str_='', int_=0, bool_=False), a2={}, a3=None)
# exp_b.a1.bool_
# exp_b.a1.str_


exp_b1 = ExampleB(**{
    "a1": {
        "str_"  : "1",
        "int_"  : 1,
        "bool_" : True,
    },
    # 给出了一个不符合类型注解的字典，所以无法替换ExampleA对象的字段
    "a2": {
        "1": "2"
    }
})
# 虽然上面只给定了 a1 字段，没给出的字段会走默认行为
print(exp_b1)
# :return: ExampleB(a1=ExampleA(str_='1', int_=1, bool_=True), a2=ExampleA(str_='', int_=0, bool_=False), a3=None)


# 示例三, 继承ExampleA
@ex_dataclass
class ExampleC(ExampleA):

    c1: str = field(default_factory=str)
    c2: ExampleB = field(default_factory=ExampleB, required=True)


exp_c = ExampleC(**{
    "c1": "aaxx",
    "c2": {
        "str_"  : "1",
        "int_"  : 1,
        "bool_" : True,
        # 冗余字段, 会被舍弃
        "float_": 0.0
    }
})

# 可以看到ExampleA的属性也被继承了
# exp_c.str_
# exp_c.c1.lower  // 因为我们给定了类型注解所以直接就可以使用str的方法
# exp_c.c2.a1.bool_ // 看看这个补全，很爽吧在编码的时候
print(exp_c)
# :return: ExampleC(str_='', int_=0, bool_=False, c1='aaxx', c2=ExampleB(a1=ExampleA(str_='', int_=0, bool_=False), a2={}, a3=None))


# 示例四，继承EXpack获得更多额外能力；
@ex_dataclass
class ExampleD(EXpack):

    str_: str = field(default_factory=str)
    int_: int = field(default=0)
    bool_: bool = field(default_factory=bool)
    #
    date: datetime.date = field(default=datetime.datetime.now())


data = {
    "str_"  : "1",
    "int_"  : 1,
    "bool_" : True,
    "date": datetime.datetime.now()
}
exp_d = ExampleD(**data)
# 可以看到date_是一个时间对象
print(exp_d)
# :return: ExampleD(str_='1', int_=1, bool_=True, date=datetime.datetime(2021, 7, 5, 22, 28, 44, 622726))
# 我们转回dict看看, 下面两个写法是等效的，第一个是由于继承EXpack获得的；
print(exp_d.asdict())
print(asdict(exp_d))
# 可以发现转回来之后date字段还是一个时间对象，而我们需要它的是一个种格式字符串，例如：2021-07-05 这样的格式
# :return: {'str_': '1', 'int_': 1, 'bool_': True, 'date': datetime.datetime(2021, 7, 5, 22, 32, 43, 198445)}

# 接下来改造一下
@ex_dataclass
class ExampleD_1(EXpack):
    str_: str = field(default_factory=str)
    int_: int = field(default=0)
    bool_: bool = field(default_factory=bool)
    #
    date: str = field(default=datetime.datetime.now())

    # 写一个函数，格式是: asdict_{filed_name}, 可以返回任意类型，返回值就是你想渲染的格式
    def asdict_date(self, value: datetime.datetime) -> typing.Any:
        return value.strftime("%Y-%m-%d")


exp_d_1 = ExampleD_1(**data)
print(exp_d_1.asdict())
# :return: {'str_': '1', 'int_': 1, 'bool_': True, 'date': '2021-07-05'}

# EXpack还提供了json_loads, json_dumps, pprint 等方法




