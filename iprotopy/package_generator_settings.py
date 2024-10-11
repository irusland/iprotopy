import dataclasses
from enum import Enum


class StringCase(Enum):
    ORIGINAL = 'ORIGINAL'
    CAMEL = 'CAMEL'
    SNAKE = 'SNAKE'
    KEBAB = 'KEBAB'
    PASCAL = 'PASCAL'


@dataclasses.dataclass
class PackageGeneratorSettings:
    service_method_name_case: StringCase = StringCase.ORIGINAL
