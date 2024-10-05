import ast
from _ast import AnnAssign, ClassDef, Load, Name, Pass, alias
from typing import List

from proto_schema_parser import Field, Message
from proto_schema_parser.ast import Comment, Enum, OneOf, Reserved

from class_field_generator import ClassFieldGenerator
from domestic_importer import DomesticImporter
from enum_generator import EnumGenerator
from imports import ImportFrom
from type_mapper import TypeMapper


class MessageClassGenerator:
    def __init__(self, importer: DomesticImporter, type_mapper: TypeMapper):
        self._importer = importer
        self._type_mapper = type_mapper

    def process_proto_message(self, current_element) -> ClassDef:
        class_body = []
        for element in current_element.elements:
            if isinstance(element, Field):
                proto_field_processor = ClassFieldGenerator(
                    self._importer, self._type_mapper
                )
                proto_field_processor.process_field(element, class_body)
            elif isinstance(element, Comment):
                # todo process comments
                continue
            elif isinstance(element, Enum):
                proto_enum_processor = EnumGenerator(self._importer)
                class_body.append(proto_enum_processor.process_enum(element))
            elif isinstance(element, OneOf):
                # todo process oneof
                continue
            elif isinstance(element, Message):
                class_body.append(self.process_proto_message(element))
            elif isinstance(element, Reserved):
                continue
            else:
                raise NotImplementedError(f'Unknown element {element}')
        if not class_body:
            class_body.append(Pass())
        self._importer.add_import(
            ImportFrom(module='dataclasses', names=[alias(name='dataclass')], level=0)
        )
        class_name = current_element.name
        class_body = self._reorder_fields(class_body)
        self._importer.register_class(class_name)
        return ClassDef(
            name=class_name,
            bases=[],
            keywords=[],
            body=class_body,
            decorator_list=[Name(id='dataclass', ctx=Load())],
        )

    def _reorder_fields(self, class_body: List[ast.stmt]) -> List[ast.stmt]:
        default_fields = []
        other_fields = []
        other_members = []
        for field in class_body:
            if isinstance(field, AnnAssign):
                if field.value is not None:
                    default_fields.append(field)
                else:
                    other_fields.append(field)
            else:
                other_members.append(field)
        return other_fields + default_fields + other_members
