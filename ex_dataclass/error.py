"""
Custom Error
"""
from ex_dataclass import m


__all__ = [
    'FieldRequiredError',
    'FieldNotMatchValueError'
]

class FieldRequiredError(Exception):

    def __init__(self, filed_name: m.F_NAME):
        self.f_name = filed_name


    def __str__(self):
        return f"{self.f_name} must be required, which is missing."



class FieldNotMatchValueError(TypeError):

    def __init__(self, filed_name: m.F_NAME, field_type: m.F_TYPE):
        self.f_name = filed_name
        self.f_type = field_type

    def __str__(self):
        return f"The <class {self.f_name}> given value type cannot match the filed type of the annotation. Expected field type: {self.f_type}"

