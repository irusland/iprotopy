import ast
import keyword
from _ast import AnnAssign, Constant, Load, Name, Store, Subscript, alias
from typing import Callable, List

from proto_schema_parser import Field, FieldCardinality

from domestic_importer import DomesticImporter
from imports import ImportFrom
from type_mapper import TypeMapper


class ProtoFieldProcessor:
    def __init__(self, importer: DomesticImporter, type_mapper: TypeMapper):
        self._importer = importer
        self._type_mapper = type_mapper

    def _process_optional_field(self, field: Field, fields):
        def get_field(safe_field_name: str, safe_field_type: str) -> AnnAssign:
            return AnnAssign(
                target=Name(id=safe_field_name, ctx=Store()),
                annotation=Subscript(
                    value=Name(id='Optional', ctx=Load()),
                    slice=Name(id=safe_field_type, ctx=Load()),
                    ctx=Load(),
                ),
                value=Constant(value=None),
                simple=1,
            )

        self._process_field_template(field, fields, get_field)
        self._importer.add_import(
            ImportFrom(module='typing', names=[alias(name='Optional')], level=0)
        )

    def process_field(self, field: Field, fields):
        if field.cardinality == FieldCardinality.REPEATED:
            self._process_repeated_field(field, fields)
        elif field.cardinality == FieldCardinality.OPTIONAL:
            self._process_optional_field(field, fields)
        else:
            self._process_single_field(field, fields)

    def _process_field_template(
        self,
        field: Field,
        fields: List[ast.stmt],
        get_field: Callable[[str, str], AnnAssign],
    ):
        safe_field_name = self._safe_field_name(field.name)
        field_type = field.type
        try:
            field_type, field_import = self._type_mapper.map(field_type)
            if field_import is not None:
                self._importer.add_import(field_import)
        except ValueError:
            if '.' in field_type:
                class_name = field_type.split('.')[0]
                self._importer.register_dependency(class_name)
            else:
                self._importer.register_dependency(field_type)
            field_type = f"'{field_type}'"

        fields.append(get_field(safe_field_name, field_type))

    def _process_repeated_field(self, field: Field, fields):
        def get_field(safe_field_name: str, safe_field_type: str) -> AnnAssign:
            return AnnAssign(
                target=Name(id=safe_field_name, ctx=Store()),
                annotation=Subscript(
                    value=Name(id='List', ctx=Load()),
                    slice=Name(id=safe_field_type, ctx=Load()),
                    ctx=Load(),
                ),
                simple=1,
            )

        self._process_field_template(field, fields, get_field)
        self._importer.add_import(
            ImportFrom(module='typing', names=[alias(name='List')], level=0)
        )

    def _process_single_field(self, field: Field, fields):
        def get_field(safe_field_name: str, safe_field_type: str) -> AnnAssign:
            return AnnAssign(
                target=Name(id=safe_field_name, ctx=Store()),
                annotation=Name(id=safe_field_type, ctx=Load()),
                simple=1,
            )

        self._process_field_template(field, fields, get_field)

    def _safe_field_name(self, unsafe_field_name: str) -> str:
        if keyword.iskeyword(unsafe_field_name):
            return f'{unsafe_field_name}_'
        return unsafe_field_name
