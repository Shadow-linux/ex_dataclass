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
                 '_field_type',  # Private: not to be used by user code.
                 )

    def __init__(self, default, default_factory, required, init, repr, hash, compare,
                 metadata):
        self.required = required

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


# # todo 后续会增加is_validate 标识开启 validate 校验
def field(*, default=MISSING, default_factory=MISSING, required=False, init=True, repr=True,
          hash=None, compare=True, metadata=None):
    """Return an object to identify dataclass fields.
    """

    if default is not MISSING and default_factory is not MISSING:
        raise ValueError('cannot specify both default and default_factory')
    return ExField(default, default_factory, required, init, repr, hash, compare,
                   metadata)


def get_field_witch_cls(cls: typing.Callable, key: str) -> typing.Optional[ExField]:
    return getattr(cls, '__dataclass_fields__').get(key)


def check_field_is_required(cls_name: str, f: ExField, f_name_list: typing.List[m.F_NAME]):
    if f.required:
        if f.name not in f_name_list:
            raise error.FieldRequiredError(f"<class '{cls_name}'>.{f.name}")
