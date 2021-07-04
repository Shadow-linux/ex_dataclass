"""
Custom Error
"""
from ex_dataclass import m


__all__ = [
    'FieldRequiredError'
]

class FieldRequiredError(Exception):

    def __init__(self, filed_name: m.F_NAME):
        self.f_name = filed_name


    def __str__(self):
        return f"{self.f_name} must be required, which is missing."

