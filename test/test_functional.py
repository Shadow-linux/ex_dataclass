import typing
import datetime
from collections import ChainMap
from ex_dataclass.ex_dataclass import ex_dataclass, field, EXpack, asdict

baseline = {'music': 'bach', 'art': 'rembrandt'}
adjustments = {'art': 'van gogh', 'opera': 'carmen'}

cmap = ChainMap(adjustments, baseline)
print(cmap.get("music"))

a :typing.List[int] = [1,2]

@ex_dataclass
class A:
    l :typing.List[typing.List[str]] = field(default_factory=list)

aa = A(**{"l": [["1"]]})

print(aa.__dict__.get("_name"))
print(aa.__annotations__['l'].__dict__.get('__args__', ()))
print(type(aa.__annotations__['l']))



def recursive_iter(layer_index: int, values: typing.List):
    pass


# handle recursive
layer_amount = 3
test_data = [[[1,2], [3,4]],[[5,6], [7,8]]]

def handle_recursive(current_layer, values: typing.List[typing.Any]) -> typing.List[typing.Any]:
    if current_layer == layer_amount:
        values.append(100)
        return values
    tmp_value_list = []
    for v in values:
        tmp_value_list.append(
                handle_recursive(current_layer + 1, v)
        )
    return tmp_value_list


print(handle_recursive(1, test_data))


# test

import types
from functools import wraps

class Profiled:
    def __init__(self, func):
        wraps(func)(self)
        self.ncalls = 0

    def __call__(self, *args, **kwargs):
        self.ncalls += 1
        return self.__wrapped__(*args, **kwargs)

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)


@Profiled
def add(x, y):
    return x + y


print(add(1, 2))
print(add.ncalls)


class ExDMeta(type):
    # Optional
    def pprint(cls):
        print(cls)





# 5.3387778809999995s


class XPackMeta(type):

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        return super().__prepare__(name, bases)

    # Required
    def __new__(cls, name, bases, ns, **kwargs):
        print(name, bases, ns)
        obj = super().__new__(cls, name, bases, ns)
        print(obj)
        return obj

    # Required
    def __init__(self, name, bases, ns, _xpack=None, **kwargs):
        super().__init__(name, bases, ns)

class B:
    pass

class A(B, metaclass=XPackMeta):

    def __init__(self):
        pass

print(A())


@ex_dataclass
class User(EXpack):
    created: datetime.datetime = field(default=datetime.datetime.now())

    name: str = field(default_factory=str, required=True)
    age: int = field(default_factory=int, required=True)
    dd: datetime.datetime = field(default=datetime.datetime.now())

    # 写一个函数，格式是: asdict_{filed_name}, 接受一个value，可以返回任意类型，返回值就是你想渲染的格式
    def asdict_created(self, value: datetime.datetime) -> typing.Any:
        return value.strftime("%Y-%m-%d")

    def asdict_dd(self, value: datetime.datetime) -> object:
        # print(field.field_name, field.field_value, field.field_type, field.type_name)
        return value.strftime("%Y-%m-%d")

u1 = User(**{"name": "jack", "age": 18})
print(u1)
print(asdict(u1))