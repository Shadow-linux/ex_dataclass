"""
需要支持的类型
typing.Set
typing.FrozenSet
typing.List
typing.Dict
typing.Tuple

typing.Union  // 待定
typing.Type

str
int
float
list
dict
tuple
set
frozenset
"""
import typing
from . import m
from .m import is_dataclass

BASIC_TYPE_LIST = [str, int, float, ]

REGISTER_TYPE_LIST = [
                         # normal container
                         list, dict,
                         # typing container
                         typing.Set, typing.List,
                         # typing significant
                         typing.Type, typing.Union
                     ] + BASIC_TYPE_LIST


def ignore_type(t: type) -> bool:
    # ~T is typing.TypeVar mean generic type
    if type(t) in (typing.TypeVar,):
        return True
    return False


def is_typing_list(ft: m.f_type) -> bool:
    return getattr(ft, '_name', None) == m.TypingList


def is_typing_dict(ft: m.f_type) -> bool:
    return getattr(ft, '_name', None) == m.TypingDict


def is_typing_union(ft: m.f_type) -> bool:
    if hasattr(ft, '__origin__'):
        return getattr(ft.__origin__, '_name', None) == m.TypingUnion
    return False

def is_typing_type(ft: m.f_type) -> bool:
    return getattr(ft, '_name', None) == m.TypingType


class Field_:

    def __init__(self,
                 e_class: type,
                 field_name: str,
                 field_value: typing.Any,
                 field_type: typing.Any):

        self.field_type = field_type
        self.field_name = field_name
        self.field_value = field_value

        self.__e_class = e_class
        self.__type_name: str = ""

        self.is_basic = False
        self.is_list = False
        self.is_dict = False
        self.is_dataclass = False
        self.is_typing_union = False
        self.is_typing_type = False

        self.is_abort = False

        self.__find_ft_with_mro()

    def __str__(self):
        return f"<class 'Field_.{self.field_name}'>"

    # when field type is none, maybe we can find file_type in mro classes
    def __find_ft_with_mro(self):
        if self.field_type is None:
            for cls_ in self.__e_class.__mro__:
                # ignore expack class
                if getattr(self, m.EXPackField, None):
                    continue
                if hasattr(cls_, "__annotations__"):
                    self.field_type = cls_.__annotations__.get(self.field_name, None)
                    if self.field_type:
                        break

        if self.field_type is None:
            self.is_abort = True

    def __ft_is_dataclass(self) -> (m.f_type, bool):
        res = is_dataclass(self.field_type)
        self.is_dataclass = res
        return "dataclass", res

    def __ft_is_basic(self) -> (m.f_type, bool):
        if self.field_type in BASIC_TYPE_LIST:
            return getattr(self.field_type, "__name__", None), True
        return getattr(self.field_type, "__name__", None), False

    def __ft_is_dict(self) -> (m.f_type, bool):
        self.is_dict = is_typing_dict(self.field_type) or self.field_type == dict
        return m.TypingDict, self.is_dict

    def __ft_is_list(self) -> (m.f_type, bool):
        self.is_list = is_typing_list(self.field_type) or self.field_type == list
        return m.TypingList, self.is_list

    def __ft_is_typing_union(self) -> (m.f_type, bool):
        self.is_typing_union = is_typing_union(self.field_type)
        return m.TypingUnion, self.is_typing_union

    def __ft_is_typing_type(self) -> (m.f_type, bool):
        self.is_typing_type = is_typing_type(self.field_type)
        return m.TypingType, self.is_typing_type

    @property
    def e_class(self):
        return self.__e_class

    @property
    def type_name(self):
        return self.__type_name

    def build(self) -> "Field_":
        if not self.is_abort and not self.is_dataclass:
            for ft_fn in (self.__ft_is_basic,
                          self.__ft_is_dataclass,
                          self.__ft_is_dict,
                          self.__ft_is_list,
                          self.__ft_is_typing_union,
                          self.__ft_is_typing_type):
                self.__type_name, ok = ft_fn()
                if ok:
                    break
            else:
                self.__type_name = self.field_type.__class__
            # todo: 是否应该限制类型?
            # else:
            #     raise Exception(f"<class 'Field_.{self.field_name}'> not support type: {self.field_type} ")

        return self
