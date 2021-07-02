# ex_dataclass

[![LICENSE](https://img.shields.io/github/license/Shadow-linux/ex_dataclass)](https://img.shields.io/github/license/Shadow-linux/ex_dataclass)
[![VERSION](https://img.shields.io/github/v/release/Shadow-linux/ex_dataclass)](https://img.shields.io/github/v/release/Shadow-linux/ex_dataclass)
[![PYPI](https://img.shields.io/pypi/v/ex-dataclass)](https://img.shields.io/pypi/v/ex-dataclass)
[![LANGUAGE](https://img.shields.io/badge/python-3.7%2B-blue)](https://img.shields.io/badge/python-3.7%2B-blue)
[![CODEBEAT](https://img.shields.io/badge/codebeat-4.00-success)](https://img.shields.io/badge/codebeat-4.00-success)
### ex_dataclass 是什么？

* 它一款继基于 `dataclass` 开发的 `python` 库，但对数据模型处理更加的友好。它通过  **Python3类型注解** 能轻易的处理 `dict` 与自定义 `class` 间的转换，从而明确复杂数据模型的类型，降低维护代码的压力及理清编码思路等作用。
* 它在配合 `Python3 typing` 模块的特殊容器的类型注解能实现更多高级功能；


### 特性

* **注解类型支持**
- [x] int
- [x] str
- [x] float
- [x] dict
- [x] list
- [x] typing.List
- [x] typing.Union
- [x] typing.Type

* **功能**
- [x] 支持 `ex_dataclass` 类型继承的正反解析；
- [x] 支持 `typing.List` 中 `ex_dataclass` 类型正反解析；
- [x] 支持 `typing.List` 嵌套正反解析，如：`{a: [[{a:1, b:2}, {a:3, b:4}]]}`
- [x] 支持 `typing.Union` 和 `typing.Type` 特殊容器类型注解的多态行为，精确匹配字段存在最多 `ex_dataclass`（类型断言上，仅支持普通pytho类型；如：int，float等）
- [x] 支持反向解析下存在冗余字段，默认行为是抛弃冗余字段（可进行配置）
- [x] 支持typing.Union 和 typing.Type 特殊容器类型相互嵌套场景 
- [ ] 支持类型注解作用于值的校验，类似参数签名，若不正确引发异常
- [ ] 支持 `ex_dataclass` 类型全属性字段名一一对应检测，若不正确引发异常


### 快速开始

> 示例 1

* [typing 模块介绍](https://juejin.cn/post/6939159210991026190)
* [typing 官方文档](https://docs.python.org/3/library/typing.html)

```python
import typing
from ex_dataclass import ex_dataclass, asdict, field, EXPack


@ex_dataclass
class User:
    # default_factory: 需要给一个类（可callable）
    name: str = field(default_factory=str)
    # default: 给定一个默认值
    age: int = field(default=0)


@ex_dataclass
class Team:
    team_name: str = field(default_factory=str)
    # 没有值时，我们设置一个list给users字段
    users: typing.List[User] = field(default_factory=list)


@ex_dataclass
class AllTeam:
    teams: typing.List[Team] = field(default_factory=list)


# 看看TeamUser 接受参数或字典

data = {
    "teams": [
        {
            "team_name": "Team-A",
            "users"    : [
                {
                    "name": "zhangsan",
                    "age" : 18,
                },
                {
                    "name": "lisi",
                    "age" : 18,
                }
            ]
        },
{
            "team_name": "Team-B",
            "users"    : [
                {
                    "name": "jack",
                    "age" : 18,
                },
                {
                    "name": "rose",
                    "age" : 18,
                }
            ]
        }
    ]
}
all_team = AllTeam(**data)
# 可以看到运行结果，所有类型都被转换成对象，对象在python中是非常的友好可以进行全方位自动补全，并且方便维护；
print(all_team)
# AllTeam(teams=[Team(team_name='Team-A', users=[User(name='', age=18), User(name='', age=18)]), Team(team_name='Team-B', users=[User(name='', age=18), User(name='', age=18)])])
print(all_team.teams)
# [Team(team_name='Team-A', users=[User(name='', age=18), User(name='', age=18)]), Team(team_name='Team-B', users=[User(name='', age=18), User(name='', age=18)])]
print(all_team.teams[0].team_name)
print(all_team.teams[0].users)
# Team-A
# [User(name='', age=18), User(name='', age=18)]
print(all_team.teams[0].users[0].name)
# zhangsan

# 重新转回字典
print(asdict(all_team))
# {'teams': [{'team_name': 'Team-A', 'users': [{'name': 'zhangsan', 'age': 18}, {'name': 'lisi', 'age': 18}]}, {'team_name': 'Team-B', 'users': [{'name': 'jack', 'age': 18}, {'name': 'rose', 'age': 18}]}]}


```

* 看完第一个示例应该能发现 `ex_dataclass` 对数据转换成对象，全凭的是我们在属性字段后面写的**类型注解**。通过这样的转换能力，我们就可以摆脱 `data_dict["a"]["b"]["c"]` 这样取值的复杂场景；

> 示例 2 
* 在继承关系中 `ex_dataclass` 依旧能准确识别你所需要转换的类型。

```python

@ex_dataclass
class Person:
    # default_factory: 需要给一个类（可callable）
    name: str = field(default_factory=str)
    # default: 给定一个默认值
    age: int = field(default=0)
    height: float = field(default=float)
    weight: float = field(default=float)


@ex_dataclass
class PersonDetails:
    address: str = field(default_factory=str)
    hobbies: typing.List[str] = field(default_factory=list)
    phone: str = field(default_factory=str)


# 继承person使其拥有person的熟悉
@ex_dataclass
class Male(Person):
    gender: str = field(default="male")


@ex_dataclass
class Female(Person):
    gender: str = field(default="female")


@ex_dataclass
class Jack(Male):
    # 当你默认值需要PersonDetails 对象时，可以写入到default_factory, 如果不需要则写dict或None
    details: PersonDetails = field(default_factory=PersonDetails)


@ex_dataclass
class Rose(Female):
    details: PersonDetails = field(default_factory=dict)


# 最终初始化两个人物，使用参数初始化, 这里并没有给出gender，因为已经设置默认值了
jack = Jack(
        name="jack",
        age=18,
        height=1.80,
        weight=125.0,
        details={
            "address": "xxxx",
            "hobbies": ["aa", "bb", "cc"],
            "phone"  : "123456789"
        }
)
# 使用字典初始化
rose = Rose(
        name="rose",
        age=18,
        height=1.680,
        weight=98.0,
        details={
            "address": "xxxx",
            "hobbies": ["aa", "bb", "cc"],
            "phone"  : "987654321"
        }
)
print(jack)
print(jack.details.phone)
print(rose)
print(rose.details.phone)
# Jack(name='jack', age=18, height=1.8, weight=125.0, gender='male', details=PersonDetails(address='xxxx', hobbies=['aa', 'bb', 'cc'], phone='123456789'))
# 123456789
# Rose(name='rose', age=18, height=1.68, weight=98.0, gender='female', details=PersonDetails(address='xxxx', hobbies=['aa', 'bb', 'cc'], phone='987654321'))
# 987654321


```

> 实例 3

* 一段复杂数据的补全







### 进阶用法


请移步: [文档]()


### 文档


### 联系方式

* 可以通过issue提出建议或意见。
* EMail: 972367265@qq.com








