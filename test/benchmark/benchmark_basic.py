from time import perf_counter as pc
from ex_dataclass.ex_dataclass import ex_dataclass, typing, field
from ex_dataclass.xpack import EXpack

b_file_1 = "basic_1.json"
b_file_1000 = "basic_1000.json"
b_file_10000 = "basic_10000.json"
# data = {"user_id": 1, "user_name": "zhangsan", "score": 100.0, "hobbies": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "skills": {"sk1": "1", "sk2": "2", "sk3": "3"}, "experience": [{"ex1": "ex1", "ex2": "ex2", "ex3": "ex3"},{"ex1": "ex1", "ex2": "ex2", "ex3": "ex3"}]}
with open(b_file_1) as fd:
    data_1 = fd.read()

with open(b_file_1000) as fd:
    data_1000 = fd.read()

with open(b_file_10000) as fd:
    data_10000 = fd.read()

def TestBench(data, is_print_data=False):
    start = pc()
    d = Data.json_loads(data)
    print(pc() - start)
    if is_print_data: print(d)

@ex_dataclass
class Skill:

    sk1: str = field(default_factory=str)
    sk2: str = field(default_factory=str)
    sk3: str = field(default_factory=str)


@ex_dataclass
class Exper1:
    ex1: str = field(default_factory=str)


@ex_dataclass
class Exper(Exper1):

    ex2: str = field(default_factory=str)
    ex3: str = field(default_factory=str)

@ex_dataclass
class Person(EXpack):

    user_id: int = field(default_factory=int)
    user_name: str = field(default_factory=str)
    score: float = field(default_factory=float)
    hobbies: typing.List[int] = field(default_factory=list)
    skills: Skill = field(default_factory=Skill)
    experience: typing.List[Exper] = field(default_factory=list)

@ex_dataclass
class Data(EXpack):

     data: typing.List[Person] = field(default_factory=list)


print()
print("=" * 50 + " basic 1 test " + "=" * 50)
for _ in range(0, 5):
    TestBench(data_1, is_print_data=False)
#
print()
print("=" * 50 + " basic 1000 test " + "=" * 50)
for _ in range(0, 5):
    TestBench(data_1000, is_print_data=False)


print()
print("=" * 50 + " basic 10000 test " + "=" * 50)
for _ in range(0, 5):
    TestBench(data_10000, is_print_data=False)


