"""
magic 主要讲typing.Union 和 typing.Type，这2个比较灵活的类型注解
"""
import typing
from ex_dataclass import ex_dataclass, asdict, field, EXpack


# =========================== typing.Union ===========================
# 多态的类的选择

@ex_dataclass
class Human:
    name: str = field(default_factory=str)
    age: int = field(default_factory=int)


@ex_dataclass
class Male:
    name: str = field(default_factory=str)
    age: int = field(default_factory=int)
    is_male: bool = field(default_factory=bool)


@ex_dataclass
class Female:
    name: str = field(default_factory=str)
    age: int = field(default_factory=int)
    is_female: bool = field(default_factory=bool)


# 开始
@ex_dataclass(ex_debug=False)
class Table:
    # 这里是想生成一个male对象，但数据有可能是以下三种情况
    want_male: typing.Union[Human, Male, Female] = field(default_factory=dict)
    # want female
    want_female: typing.Union[Human, Male, Female] = field(default_factory=dict)
    # want human
    want_people: typing.Union[Human, Male, Female] = field(default_factory=dict)


tb1 = Table(**{
    "want_people": {"name": "human",
                    "age" : 18,
                    },
    "want_male"  : {"name"   : "male",
                    "age"    : 18,
                    "is_male": True, },
    "want_female": {"name"     : "female",
                    "age"      : 18,
                    "is_female": True, },
})

# 可以看到ex_dataclass 为这三种数据准确的生成了各自对象
print(tb1)
# Table(want_male=Male(name='male', age=18, is_male=True), want_female=Female(name='female', age=18, is_female=True), want_people=Human(name='human', age=18))


# =========================== typing.Type ===========================

# typing.Type 其实通过子类寻找之间的关系


@ex_dataclass
class Human:
    name: str = field(default_factory=str)
    age: int = field(default_factory=int)


# 使用了继承
@ex_dataclass
class Male(Human):
    is_male: bool = field(default_factory=bool)


@ex_dataclass
class Female(Human):
    is_female: bool = field(default_factory=bool)


# 开始
@ex_dataclass(ex_debug=False)
class Table2:
    # 这的写法只需要标记出它的父类，子类也会被寻找到
    want_male: typing.Type[Human] = field(default_factory=dict)
    # want female
    want_female: typing.Type[Human] = field(default_factory=dict)
    # want Human
    want_people: typing.Type[Human] = field(default_factory=dict)


tb2 = Table2(**{
    "want_people": {"name": "people",
                    "age" : 18,
                    },

    "want_male"  : {"name"   : "male",
                    "age"    : 18,
                    "is_male": True, },

    "want_female": {"name"     : "female",
                    "age"      : 18,
                    "is_female": True, },
})

# 可以看到ex_dataclass 为这三种数据准确的生成了各自对象
print(tb2)
# Table2(want_male=Male(name='male', age=18, is_male=True),
#        want_female=Female(name='female', age=18, is_female=True),
#        want_people=Human(name='people', age=18))

# 断言看看类型是否相等
assert type(tb2.want_female) == Female, True
assert type(tb2.want_male) == Male, True
assert type(tb2.want_people) == Human, True


# =========================== typing.Type 和 typing.Union 在 typing.List中使用 ===========================

# super man 不继承Human, 毕竟他不是人类
@ex_dataclass
class SuperMan:
    name: str = field(default_factory=str)
    age: int = field(default=100)
    xray: bool = field(default=True)
    fly: bool = field(default=True)
    fast: bool = field(default=True)
    smart: bool = field(default=True)


@ex_dataclass(ex_debug=False)
class Table3():
    list_a: typing.List[typing.Type[Human]] = field(default_factory=list)
    # 下面加入了SuperMan
    list_b: typing.List[typing.Union[Human, Male, Female, SuperMan]] = field(default_factory=list)


tb3 = Table3(**{
    "list_a": [
        # male
        {"name": "male", "age": 18, "is_male": True},
        # female
        {"name": "female", "age": 18, "is_female": True}
    ],
    "list_b": [
        # male
        {"name": "male", "age": 18, "is_male": True},
        # female
        {"name": "female", "age": 18, "is_female": True},
        # superman
        {"name": "female", "age": 18, "xray": True, "fly": True, "fast": True, "smart": True}
    ]
})
print(tb3)
# Table3(list_a=[Male(name='male', age=18, is_male=True),
#               Female(name='female', age=18, is_female=True)],
#        list_b=[Male(name='male', age=18, is_male=True),
#               Female(name='female', age=18, is_female=True),
#               SuperMan(name='female', age=18, xray=True, fly=True, fast=True, smart=True)])


# 通过类型断言，每个数据都正常的转回我们需要的对象
assert type(tb3.list_a[0]) == Male, True
assert type(tb3.list_a[1]) == Female, True
assert type(tb3.list_b[0]) == Male, True
assert type(tb3.list_b[1]) == Female, True
assert type(tb3.list_b[2]) == SuperMan, True


from collections import namedtuple
