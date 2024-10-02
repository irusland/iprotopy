import ast
import keyword
import logging
from ast import Store, Load, ClassDef, alias, AnnAssign, Name, Subscript, Constant, Module, Assign, Pass
from pathlib import Path
from types import NoneType
from typing import Union, Tuple, List, Set

import astor
from proto_schema_parser.ast import (
    File, Message, Field, MessageElement, Comment, Enum,
    EnumValue, Package, Option, Service, OneOf, Reserved, Extension, FieldCardinality,
)
from proto_schema_parser.ast import Import as ProtoImport
from proto_schema_parser.parser import Parser

from paths import ROOT_DIR
from src.imports import Import, ImportFrom

logger = logging.getLogger(__name__)

AstImport = Union[Import, ImportFrom]


class TypeMapper:
    def __init__(self):
        self._standard_types_mapping = {
            'string': 'str',
            'int64': 'int',
            'int32': 'int',
        }

        self._google_types_mapping = {
            'google.protobuf.Timestamp': ('datetime', Import(module='datetime', names=[alias(name='datetime')], level=0))
        }

    def map(self, proto_type: str) -> Tuple[str, Union[AstImport, None]]:
        if proto_type in self._standard_types_mapping:
            return self._standard_types_mapping[proto_type], None
        if proto_type in self._google_types_mapping:
            return self._google_types_mapping[proto_type]
        return f"'{proto_type}'", None
        raise NotImplementedError(f'Unknown type {proto_type}')


class Generator:
    def __init__(self, parser: Parser, type_mapper: TypeMapper):
        self._parser = parser
        self._type_mapper = type_mapper

    def generate_sources(self, proto_dir: Path, out_dir: Path):
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / '__init__.py').touch()
        for proto_file in proto_dir.rglob('*.proto'):

            pyfile = proto_file.relative_to(proto_dir).with_suffix('.py')

            logger.debug(pyfile)
            self.generate_source(proto_file, out_dir, pyfile)

    def _safe_field_name(self, unsafe_field_name: str) -> str:
        if keyword.iskeyword(unsafe_field_name):
            return f'{unsafe_field_name}_'
        return unsafe_field_name

    def generate_source(self, proto_file: Path, out_dir: Path, pyfile: Path):
        logger.debug(f'Generating source for {proto_file}')
        with open(proto_file) as f:
            text = f.read()

        result: File = self._parser.parse(text)

        body = []
        imports = set()
        for element in result.file_elements:
            if isinstance(element, Message):
                self._process_proto_message(body, element, imports)
            elif isinstance(element, Package):
                continue
            elif isinstance(element, Option):
                continue
            elif isinstance(element, ProtoImport):
                continue
            elif isinstance(element, Service):
                # todo process services
                continue
            elif isinstance(element, Comment):
                continue
            elif isinstance(element, Enum):
                self._process_enum(body, element, imports)
            elif isinstance(element, NoneType):
                continue
            elif isinstance(element, Extension):
                continue
            else:
                raise NotImplementedError(f'Unknown element {element}')
        module = Module(
            body=list(imports) + body, type_ignores=[]
        )

        result_src = astor.to_source(module)

        (out_dir / pyfile).parent.mkdir(parents=True, exist_ok=True)
        with open(out_dir / pyfile, 'w') as f:
            f.write(result_src)

    def _process_proto_message(self, body: List[ast.stmt], message, imports: Set[ast.stmt]):
        if message.name == 'GetBondEventsResponse':
            print(message)
        class_body = []
        for element in message.elements:
            if message.name == 'GetBondEventsResponse':
                print(element)
            if isinstance(element, Field):
                self._process_field(element, class_body, imports)
            elif isinstance(element, Comment):
                # todo process comments
                continue
            elif isinstance(element, Enum):
                self._process_enum(class_body, element, imports)
            elif isinstance(element, OneOf):
                # todo process oneof
                continue
            elif isinstance(element, Message):
                self._process_proto_message(class_body, element, imports)
            elif isinstance(element, Reserved):
                continue
            else:
                raise NotImplementedError(f'Unknown element {element}')
        if not class_body:
            class_body.append(Pass())
        imports.add(ImportFrom(module='dataclasses', names=[alias(name='dataclass')], level=0))
        body.append(
            ClassDef(
                name=message.name,
                bases=[],
                keywords=[],
                body=class_body,
                decorator_list=[Name(id='dataclass', ctx=Load())]
            )
        )

    def _process_enum(self, body, element, imports):
        enum_body = []
        for enum_element in element.elements:
            if isinstance(enum_element, EnumValue):
                enum_body.append(
                    Assign(
                        targets=[Name(id=enum_element.name, ctx=Store())],
                        value=Constant(value=enum_element.number)
                    ),
                )
            elif isinstance(enum_element, Comment):
                # todo process comments
                continue
            else:
                raise NotImplementedError(f'Unknown enum_element {enum_element}')

        imports.add(ImportFrom(module='enum', names=[alias(name='Enum')], level=0))
        enum_class = ClassDef(
            name=element.name,
            bases=[Name(id='Enum', ctx=Load())],
            keywords=[],
            body=enum_body,
            decorator_list=[]
        )
        body.append(enum_class)

    def _process_field(self, field: Field, fields, imports: Set[AstImport]):
        if field.cardinality == FieldCardinality.REPEATED:
            self._process_repeated_field(field, fields, imports)
        elif field.cardinality == FieldCardinality.OPTIONAL:
            self._process_optional_field(field, fields, imports)
        else:
            self._process_single_field(field, fields, imports)

    def _process_optional_field(self, field: Field, fields, imports: Set[AstImport]):
        field_name = self._safe_field_name(field.name)
        field_type, field_import = self._type_mapper.map(field.type)
        fields.append(
            AnnAssign(
                target=Name(id=field_name, ctx=Store()),
                annotation=Subscript(
                    value=Name(id='Optional', ctx=Load()),
                    slice=Name(id=field_type, ctx=Load()), ctx=Load()
                ), value=Constant(value=None), simple=1
            )
        )
        if field_import is not None:
            imports.add(field_import)
        imports.add(ImportFrom(module='typing', names=[alias(name='Optional')], level=0))

    def _process_repeated_field(self, field: Field, fields, imports: Set[AstImport]):
        field_name = self._safe_field_name(field.name)
        field_type, field_import = self._type_mapper.map(field.type)
        fields.append(
            AnnAssign(
                target=Name(id=field_name, ctx=Store()),
                annotation=Subscript(
                    value=Name(id='List', ctx=Load()),
                    slice=Name(id=field_type, ctx=Load()), ctx=Load()
                ), simple=1
            )
        )
        if field_import is not None:
            imports.add(field_import)
        imports.add(ImportFrom(module='typing', names=[alias(name='List')], level=0))

    def _process_single_field(self, field: Field, fields, imports: Set[AstImport]):
        field_name = self._safe_field_name(field.name)
        field_type, field_import = self._type_mapper.map(field.type)
        fields.append(
            AnnAssign(
                target=Name(id=field_name, ctx=Store()),
                annotation=Name(id=field_type, ctx=Load()), simple=1
            )
        )
        if field_import is not None:
            imports.add(field_import)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    parser = Parser()
    type_mapper = TypeMapper()
    gen = Generator(parser, type_mapper)
    gen.generate_sources(
        proto_dir=ROOT_DIR / 'tinkoff/invest/grpc',
        out_dir=ROOT_DIR / 'src' / "models",
    )