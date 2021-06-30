"""
core handler
"""
import typing
from abc import abstractmethod, ABCMeta

from . import m
from .m import is_dataclass
from src import type_
from src.type_ import Field_, ignore_type


class _FieldTyping(m.ToolImpl, metaclass=ABCMeta):
    debug = False
    # field type name
    FT_NAME: str = ""

    def __init__(self, f: Field_):
        super(_FieldTyping, self).__init__()
        self.f = f

    # get attribute filed type from container type
    def get_attr_field_types(self) -> typing.Tuple[m.DataClassType]:
        attr_field_types = self.f.field_type.__dict__.get('__args__', ())
        if self.debug:
            print(f"{self.f}.attr_field_types: {attr_field_types}")
        return attr_field_types

    def get_ft_attr(self, ft: m.DataClassType) -> typing.Dict[m.f_name, m.f_type]:
        return ft.__dict__['__annotations__']

    def __calculate_best_chosen(self, ft: m.f_type, max_score: int) -> typing.Tuple[m.f_type, int]:
        score = 0

        if is_dataclass(ft):
            # others
            # get DataClassType's attributes, return data format: typing.Dict[name, f_type]
            attr_dict = self.get_ft_attr(ft)
            # compare 'DataClassType',  which has the most attribute
            for key, value in self.f.field_value.items():
                attr_ft = attr_dict.get(key, None)
                if attr_ft:
                    # todo 这一个类型断言的方法并不完善，可能影响性能且不能判断全部类型；
                    if attr_ft in type_.BASIC_TYPE_LIST:
                        if isinstance(value, attr_ft):
                            score += 1.1
                    else:
                        score += 1

            if score > max_score:
                max_score = score
                return ft, max_score

        # special container typing.Type
        if type_.is_typing_type(ft):
            ftt = FieldTypingType(Field_(e_class=self.f.e_class, field_type=ft, field_value=self.f.field_value,
                                         field_name=self.f.field_name))
            ftt.handle()
            return self.__calculate_best_chosen(ftt.smart_ft, max_score)

        return ft, max_score

    # get compatibility field type
    def smart_choice_ft(self,
                        attr_field_types: typing.List[m.DataClassType]) -> typing.Optional[m.DataClassType]:
        return_ft: m.DataClassType = None
        max_score = 0

        if self.debug:
            print(f"{self.f}.chosen_types: {attr_field_types}")
            print(f"{self.f}.smart_choice_ft.field_value: {self.f.field_value}")

        for ft in attr_field_types:
            tmp_return_ft, tmp_max_score = self.__calculate_best_chosen(ft, max_score)
            if tmp_max_score > max_score:
                max_score = tmp_max_score
                return_ft = tmp_return_ft

        if self.debug:
            print(f"{self.f}.smart_choice_ft: {return_ft}, score: {max_score}")

        return return_ft

    @abstractmethod
    def handle(self, *args, **kwargs):
        raise NotImplementedError


class FieldTypingType(_FieldTyping):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.smart_ft: m.DataClassType = None

    def handle(self) -> typing.Union[m.DataClassObj, typing.Any]:
        attr_field_types = self.get_attr_field_types()

        if attr_field_types:
            # get the first generic field type
            generic_field_type = attr_field_types[0]
            self.smart_ft = self.smart_choice_ft(generic_field_type.__subclasses__() + [generic_field_type])
            if self.smart_ft:
                return self.smart_ft(**self.f.field_value)

        return self.f.field_value


class FieldTypingUnion(_FieldTyping):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.smart_ft: m.DataClassType = None

    def handle(self) -> typing.Union[m.DataClassObj, typing.Any]:
        attr_field_types = self.get_attr_field_types()

        self.smart_ft = self.smart_choice_ft(list(attr_field_types))
        if self.smart_ft:
            return self.smart_ft(**self.f.field_value)

        return self.f.field_value


class FieldTypingList(_FieldTyping):
    FT_NAME = m.TypingList

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.iterator_impl: IteratorImplement = None

    def __handle_typing_type(self, attr_ft: type) -> typing.Optional[m.DataClassType]:
        # try to get smart type
        if self.f.field_value:
            attr_f_obj = Field_(e_class=self.f.e_class, field_name=self.f.field_name,
                                field_type=attr_ft, field_value=self.f.field_value[0]).build()
            if attr_f_obj.is_typing_type:
                ftt = FieldTypingType.with_debug(self.debug, attr_f_obj)
                ftt.handle()
                return ftt.smart_ft
        return None

    def __handle_typing_union(self, attr_ft: type) -> typing.Optional[m.DataClassType]:
        # try to get smart type
        if self.f.field_value:
            attr_f_obj = Field_(e_class=self.f.e_class, field_name=self.f.field_name,
                                field_type=attr_ft, field_value=self.f.field_value[0]).build()
            if attr_f_obj.is_typing_union:
                ftu = FieldTypingUnion.with_debug(self.debug, attr_f_obj)
                ftu.handle()
                return ftu.smart_ft
        return None

    def handle(self) -> typing.List[object]:

        if getattr(self.f.field_type, "_name", None) == self.FT_NAME:
            self.iterator_impl = IteratorImplement.with_debug(self.debug, self.f)
            res_fv_list = self.iterator_impl.gen_values()

        else:
            # todo 支持python3.9 新类型注解: list[int], 后面需重构
            res_fv_list = self.f.field_value
        return res_fv_list


# handle 'list' recursive container
class IteratorImplement(m.ToolImpl):
    # just support type 'list'
    REGISTER_CONTAINER_TYPE = [m.TypingList, ]

    def __init__(self, f: Field_):
        super(IteratorImplement, self).__init__()
        self.f = f
        self.is_recursive_iterator = False
        self.__layer_container_types: typing.List[str] = []
        # recognize the first filed type
        self.__recognize_layer_type(self.f.field_type)
        self.__container_attr_type: m.f_type = self.__find_the_container_attribute_type(self.f.field_type)
        self.__layer_amount: int = 0
        # container attribute type
        self.__cat_isdataclass = False
        if is_dataclass(self.__container_attr_type):
            self.__cat_isdataclass = True

    # find the deepest attribute_type like: typing.List[typing.List[<DataClassType>]]
    # we should find the <DataClassType>
    def __find_the_container_attribute_type(self, ft: m.f_type) -> typing.Optional[m.f_type]:
        attr_field_types = ft.__dict__.get('__args__', ())
        if self.debug:
            print(f"{self.f}.attr_field_types: {attr_field_types}")

        if attr_field_types:
            if self.__recognize_layer_type(attr_field_types[0]):
                return self.__find_the_container_attribute_type(attr_field_types[0])

            if ignore_type(attr_field_types[0]): return None

            return attr_field_types[0]

        return None

    def __recognize_layer_type(self, cur_ft: type) -> bool:
        for container_type in self.REGISTER_CONTAINER_TYPE:
            if getattr(cur_ft, "_name", None) == container_type:
                self.__layer_container_types.append(container_type.lower())
                return True
        return False

    def __handle_typing_union(self, f: Field_) -> typing.Optional[m.f_type]:
        ftu = FieldTypingUnion.with_debug(self.debug, f)
        ftu.handle()
        return ftu.smart_ft

    def __handle_typing_type(self, f: Field_) -> typing.Optional[m.f_type]:
        ftt = FieldTypingType.with_debug(self.debug, f)
        ftt.handle()
        return ftt.smart_ft

    # handle the bottommost attribute like: typing.List[typing.List[ExClassA]], ExClassA is the bottommost attribute
    def __inner_container_attr_value(self, values: typing.List[typing.Any]) -> typing.List[typing.Any]:
        if self.__cat_isdataclass:
            tmp_value_list = []
            for v in values:
                tmp_value_list.append(self.__container_attr_type(**v))

            return tmp_value_list

        # judge typing type | union
        if values:
            tmp_value_list = []
            if type_.is_typing_union(self.__container_attr_type):
                for idx, v in enumerate(values):

                    ex_ft = self.__handle_typing_union(Field_(e_class=self.f.e_class,
                                                              field_name=self.f.field_name,
                                                              field_type=self.__container_attr_type,
                                                              field_value=values[idx]
                                                              ).build())
                    if ex_ft: tmp_value_list.append(ex_ft(**v))

                return tmp_value_list

            if type_.is_typing_type(self.__container_attr_type):
                for idx, v in enumerate(values):

                    ex_ft = self.__handle_typing_type(Field_(e_class=self.f.e_class,
                                                             field_name=self.f.field_name,
                                                             field_type=self.__container_attr_type,
                                                             field_value=values[idx]
                                                             ).build())
                    if ex_ft: tmp_value_list.append(ex_ft(**v))

                return tmp_value_list

        return values

    def __handle_recursive(self, current_layer, values: typing.List[typing.Any]) -> typing.List[typing.Any]:
        if current_layer == self.__layer_amount:
            if self.__container_attr_type:
                return self.__inner_container_attr_value(values)
            return values

        tmp_value_list = []
        for v in values:
            tmp_value_list.append(
                    self.__handle_recursive(current_layer + 1, v)
            )
        return tmp_value_list

    @property
    def layer_amount(self):
        return self.__layer_amount

    @property
    def container_attr_type(self):
        return self.__container_attr_type

    def gen_values(self) -> typing.List[typing.Any]:
        self.__layer_amount = len(self.__layer_container_types)
        self.is_recursive_iterator = self.__layer_amount > 1
        if self.debug:
            print(f"{self.f}.container_attr_type: {self.container_attr_type}")
            print(f"{self.f}.is_recursive_iterator: {self.is_recursive_iterator}")
            print(f"{self.f}.__layer_amount: {self.layer_amount}")

        res = self.__handle_recursive(current_layer=1, values=self.f.field_value)
        return res


class Core:
    DEBUG = False

    @classmethod
    def handle_list_type(cls, f: Field_) -> typing.Optional[typing.List[object]]:
        if f.is_list:
            ftl = FieldTypingList.with_debug(cls.DEBUG, f)
            res = ftl.handle()
            return res

        return None

    @classmethod
    def handle_dataclass_type(cls, f: Field_) -> typing.Optional[m.DataClassObj]:
        if f.is_dataclass:
            return f.field_type(**f.field_value)
        return None

    @classmethod
    def handle_dict_type(cls, f: Field_) -> typing.Optional[typing.Dict]:
        if f.is_dict:
            return f.field_value
        return None

    @classmethod
    def handle_typing_union(cls, f: Field_) -> typing.Optional[m.DataClassObj]:
        if f.is_typing_union:
            ftu = FieldTypingUnion.with_debug(cls.DEBUG, f)
            return ftu.handle()
        return None

    @classmethod
    def handle_typing_type(cls, f: Field_) -> typing.Optional[m.DataClassObj]:
        if f.is_typing_type:
            ftt = FieldTypingType.with_debug(cls.DEBUG, f)
            return ftt.handle()
        return None

    @classmethod
    def handle_default_type(cls, f: Field_) -> typing.Optional[object]:
        return f.field_value

    @classmethod
    def handle(cls, f: Field_) -> object:
        if cls.DEBUG:
            print(f"{f}.type_name: {f.type_name}")
            print(f"{f}.field_type: {f.field_type}")
            print(f"{f}.field_value: {f.field_value}")

        for h in (
                cls.handle_dataclass_type,
                cls.handle_list_type,
                cls.handle_dict_type,
                cls.handle_typing_union,
                cls.handle_typing_type,
                cls.handle_default_type,
        ):
            obj = h(f)
            if obj:
                return obj

        # If it cannot be processed, return to the original value
        return f.field_value
