"""
wrap ex_dataclass field
"""
import typing
from dataclasses import MISSING, Field
from ex_dataclass import m, error

__all__ = [
    'ExField',
    'field',
    'get_field_witch_cls'
]


class ExField(Field):
    __slots__ = ('name',
                 'type',
                 'default',
                 'default_factory',
                 'required',
                 'repr',
                 'hash',
                 'init',
                 'compare',
                 'metadata',
                 'asdict_factory',
                 'loads_factory',
                 'label',  # label: json data's key
                 '_field_type',  # Private: not to be used by user code.
                 )

    def __init__(self,
                 default,
                 default_factory,
                 required: bool,
                 label: str,
                 asdict_factory: m.asdict_func_type,
                 loads_factory: m.loads_func_type,
                 init,
                 repr,
                 hash,
                 compare,
                 metadata):
        self.required = required
        self.label = label
        self.asdict_factory = asdict_factory
        self.loads_factory = loads_factory

        self._field_type = None
        super().__init__(default, default_factory, init, repr, hash, compare,
                         metadata)

    #
    def __repr__(self):
        return ('Field('
                f'name={self.name!r},'
                f'type={self.type!r},'
                f'default={self.default!r},'
                f'default_factory={self.default_factory!r},'
                f'required={self.required},'
                f'label={self.label},'
                f'init={self.init!r},'
                f'repr={self.repr!r},'
                f'hash={self.hash!r},'
                f'compare={self.compare!r},'
                f'metadata={self.metadata!r},'
                f'_field_type={self._field_type}'
                ')')

    # def is_required(self) -> bool:
    #     return self.required
    #
    # def is_omit_empty(self) -> bool:
    #     return self.omit_empty


# # todo ???????????????is_validate ???????????? validate ??????
def field(*,
          default=MISSING,
          default_factory=MISSING,
          required: bool = False,
          label: str = None,
          asdict_factory: m.asdict_func_type = None,
          loads_factory: m.loads_func_type = None,
          init=True, repr=True,
          hash=None, compare=True, metadata=None):
    """Return an object to identify dataclass fields.
    """

    if default is not MISSING and default_factory is not MISSING:
        raise ValueError('cannot specify both default and default_factory')
    return ExField(default,
                   default_factory,
                   required,
                   label,
                   asdict_factory,
                   loads_factory,
                   init,
                   repr,
                   hash,
                   compare,
                   metadata)


def get_field_witch_cls(cls: typing.Callable, key: str) -> typing.Optional[ExField]:
    return getattr(cls, '__dataclass_fields__').get(key)


def check_field_is_required(cls_name: str, f: ExField, f_name_list: typing.List[m.F_NAME]):
    if f.required:
        if f.name not in f_name_list:
            raise error.FieldRequiredError(f"<class '{cls_name}'>.{f.name}")
