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
