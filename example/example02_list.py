"""
typing.List 列表示例，这也是ex_dataclass 比较重要的能力之一
"""
import typing
from ex_dataclass import ex_dataclass, asdict, field, EXpack


# ===================================== 示例一 =====================================

@ex_dataclass
class User:
    name: str = field(default_factory=str)
    age: int = field(default_factory=int)


@ex_dataclass
class ExampleList_1:
    # 默认值设置一个空的list
    a_list: typing.List[str] = field(default_factory=list)
    users: typing.List[User] = field(default_factory=list)


# 第一种写法
exp_list_1 = ExampleList_1(**{
    "a_list": ["a", "b", "c"],
    "users" : [
        # 两个user字典
        {"name": "zhangsan", "age": 18, },
        {"name": "lisi", "age": 18, },
    ]
})

# 可以看到users列表里面都是一个个的user对象
print(exp_list_1)
# :return: ExampleList_1(a_list=['a', 'b', 'c'], users=[User(name='zhangsan', age=18), User(name='lisi', age=18)])
# exp_list_1.users[0].name   // 可以顺利的通过补全获取到值

# 第二种写法
tmp_list = [
    # 两个user对象，
    User(**{"name": "zhangsan", "age": 18, }),
    User(**{"name": "lisi", "age": 18, }),
]
exp_list_2 = ExampleList_1(**{
    "a_list": ["a", "b", "c"],
    "users" : tmp_list
})

# 结果也是一样的
print(exp_list_2)


# :return: ExampleList_1(a_list=['a', 'b', 'c'], users=[User(name='zhangsan', age=18), User(name='lisi', age=18)])


# ===================================== 示例二 =====================================

# 嵌套列表
@ex_dataclass
class ExampleList_2:
    # 这里只展示2层，你喜欢随意你几层
    users: typing.List[typing.List[User]] = field(default_factory=list)


data = {
    "users": [
        [
            {"name": "a", "age": 18},
            {"name": "b", "age": 18},
        ],
        [
            {"name": "c", "age": 18},
            {"name": "d", "age": 18},
        ],
    ]
}


exp_list_2 = ExampleList_2(**data)
# 结果和我们设想相符合全变成对象了
print(exp_list_2)
# :return: ExampleList_2(users=[[User(name='a', age=18), User(name='b', age=18)],
# [User(name='c', age=18), User(name='d', age=18)]])
# exp_list_2.users[0][0].name // 正常获取
# exp_list_2.users[0][1].name
print(asdict(exp_list_2))

