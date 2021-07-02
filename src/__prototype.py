"""
The original version
"""
import typing
import json
from dataclasses import dataclass, is_dataclass


def ex_dataclass(*args, **kwargs):

    def wrapper(check_class):

        # passing class to investigate
        check_class = dataclass(check_class, **kwargs)
        if not hasattr(check_class, '__annotations__'):
            raise Exception(f"type obejct {check_class.__name__} missing required attribute.")
        o_init = check_class.__init__

        def __get_typing_type_subclasses(type_: typing.Type) -> typing.List[typing.Type]:
            subclasses = []
            if hasattr(type_, '_name'):
                if type_._name == "Type":
                    subclasses = type_.__dict__['__args__'][0].__subclasses__()

            return subclasses

        def __get_class_from_typing_type(type_: object) -> typing.ClassVar:
            return type_.__dict__['__args__'][0]

        def __get_cls_attr(cls: typing.Callable) -> typing.Dict:
            return cls.__dict__['__annotations__']

        def __get_high_compatibility_cls(subclass: typing.List[typing.Callable], value: typing.Dict) -> typing.Callable:
            ret_cls: typing.Callable = None
            max_cnt = 0
            for cls in subclass:
                tmp_cnt = 0
                attr_dict = __get_cls_attr(cls)
                for k, v in value.items():
                    v_type = attr_dict.get(k, None)
                    if v_type:
                        if isinstance(v, v_type):
                            tmp_cnt += 1

                if tmp_cnt > max_cnt:
                    max_cnt = tmp_cnt
                    ret_cls = cls

            return ret_cls

        def __get_all_cls_typing_type(typing_type_ft: typing.ClassVar) -> typing.List[typing.Type]:
            if typing_type_ft:
                classes = __get_typing_type_subclasses(typing_type_ft)
                if classes:
                    classes.append(__get_class_from_typing_type(typing_type_ft))
                    return classes
            return []

        def __handle_typing_list(field_type: typing.Callable, value: typing.List) -> typing.List:
            tmp_list = []
            if field_type.__dict__.get('_name', None) == 'List':
                ft_tuple = field_type.__dict__.get('__args__', ())
                if ft_tuple:
                    v = value
                    if value:
                        v = value[0] if isinstance(value[0], list) else value
                    return __handle_typing_list(ft_tuple[0], v)
                return value

            ft_cls = field_type
            # print(f"sub_type: {s_type}")
            all_classes = __get_all_cls_typing_type(ft_cls)
            if all_classes:
                for v in value:
                    # print(f"v.__class__: {v.__class__}")
                    if ft_cls == v.__class__:
                        tmp_list.append(v)
                    else:
                        ft_cls = __get_high_compatibility_cls(all_classes, v)
                        if ft_cls:
                            tmp_list.append(ft_cls(**v))
            elif is_dataclass(ft_cls):
                for v in value:
                    if ft_cls == v.__class__:
                        tmp_list.append(v)
                    else:
                        tmp_list.append(ft_cls(**v))
            else:
                tmp_list = value

            return tmp_list

        def __calculate_recursive_layer(value: typing.List, deal_with_value: typing.List) -> typing.List:
            if isinstance(value, list):
                if value:
                    if not isinstance(value[0], list):
                        return deal_with_value
                return [__calculate_recursive_layer(value[0], deal_with_value)]

            return []

        def json_loads(cls, json_data: str) -> typing.Callable:
            return cls(**json.loads(json_data))

        def __init__(self, *args, **kwargs):

            tmp_kwargs = {}
            tmp_kwargs.update(kwargs)
            for name, value in kwargs.items():

                # print(name)
                # getting field type
                field_type = check_class.__annotations__.get(name, None)
                if field_type is None:
                    for cls_ in check_class.__mro__:
                        if hasattr(cls_, "__annotations__"):
                            field_type = cls_.__annotations__.get(name, None)
                            if field_type:
                                break
                    else:
                        tmp_kwargs.pop(name)

                # 支持类型 typing.Type
                all_maybe_cls = __get_all_cls_typing_type(field_type)
                if all_maybe_cls:
                    field_type = __get_high_compatibility_cls(all_maybe_cls, value)

                # 支持类型 typing.List & 嵌套typing.List[typing.List[str]]
                if field_type is not None and isinstance(value, list):
                    tmp_kwargs[name] = __calculate_recursive_layer(value, __handle_typing_list(field_type, value))

                if is_dataclass(field_type) and isinstance(value, dict):
                    obj = field_type(**value)
                    tmp_kwargs[name] = obj
            # print(f"tmp_kwargs: {tmp_kwargs}")
            o_init(self, *args, **tmp_kwargs)

        check_class.__init__ = __init__
        # 加入json_loads
        check_class.json_loads = classmethod(json_loads)

        return check_class

    return wrapper(args[0]) if args else wrapper
