import ast
import keyword
import logging
from _ast import (
    Module, AnnAssign, Pass, alias, ClassDef, Name, Load, Assign, Store,
    Constant, Subscript,
)
from ast import (
    Store, Load, ClassDef, alias, AnnAssign, Name, Subscript, Constant,
    Module, Assign, Pass,
)
from pathlib import Path
from types import NoneType
from typing import Union, Tuple, List, Set, Dict, Callable

import astor
from proto_schema_parser import Message, Option, Field, FieldCardinality
from proto_schema_parser.ast import (
    File, Message, Field, Comment, Enum,
    EnumValue, Package, Option, Service, OneOf, Reserved, Extension, FieldCardinality,
    Import as ProtoImport,
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
            'double': 'float',
            'bool': 'bool',
        }

        self._google_types_mapping = {
            'google.protobuf.Timestamp': ('datetime', Import(
                module='datetime', names=[alias(name='datetime')], level=0
            ))
        }

    def map(self, proto_type: str) -> Tuple[str, Union[AstImport, None]]:
        if proto_type in self._standard_types_mapping:
            return self._standard_types_mapping[proto_type], None
        if proto_type in self._google_types_mapping:
            return self._google_types_mapping[proto_type]
        raise ValueError(f'Unknown type {proto_type}')


class Importer:
    def __init__(self):
        self._classes: Dict[str, Path] = {}
        self._dependencies: Dict[Path, Set[str]] = {}
        self._default_dependencies = set(i.__name__ for i in (int, str, bool))
        self._imports: Dict[Path, Set[AstImport]] = {}

    def register_class(self, class_name: str, pyfile: Path):
        if class_name in self._classes:
            logger.warning('Class %s already registered', class_name)
        self._classes[class_name] = pyfile

    def register_dependency(self, class_name: str, pyfile: Path):
        if class_name in self._default_dependencies:
            return
        dependencies = self._dependencies.get(pyfile, set())
        dependencies.add(class_name)
        self._dependencies[pyfile] = dependencies

    def get_dependency_imports(self, pyfile: Path) -> Set[AstImport]:
        dependencies_imports = {
            self._get_import_for(class_name, pyfile) for class_name in
                self._dependencies.get(pyfile,())
        }
        for import_ in self._imports.get(pyfile, ()):
            dependencies_imports.add(import_)
        return dependencies_imports

    def _get_import_for(self, class_name: str, pyfile: Path) -> AstImport:
        if class_name not in self._classes:
            raise ValueError(f'Class {class_name} not registered but requested in {pyfile}')
        return ImportFrom(
            module=self._classes[class_name].stem, names=[alias(name=class_name)],
            level=0
        )

    def remove_circular_dependencies(self):
        for class_name, pyfile in self._classes.items():
            dependencies = self._dependencies.get(pyfile, set())

            if class_name in dependencies:
                dependencies.remove(class_name)

    def add_import(self, import_statement: AstImport, pyfile: Path):
        imports = self._imports.get(pyfile, set())
        imports.add(import_statement)
        self._imports[pyfile] = imports


class ProtoEnumProcessor:
    def __init__(self, importer: Importer, pyfile: Path):
        self._importer = importer
        self._pyfile = pyfile

    def process_enum(self, element) -> ClassDef:
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

        self._importer.add_import(ImportFrom(module='enum', names=[alias(name='Enum')], level=0), self._pyfile)
        enum_name = element.name
        self._importer.register_class(enum_name, self._pyfile)
        return ClassDef(
            name=enum_name,
            bases=[Name(id='Enum', ctx=Load())],
            keywords=[],
            body=enum_body,
            decorator_list=[]
        )


class ProtoFieldProcessor:
    def __init__(self, importer: Importer, pyfile: Path, type_mapper: TypeMapper):
        self._importer = importer
        self._pyfile = pyfile
        self._type_mapper = type_mapper

    def _process_optional_field(
        self, field: Field, fields
    ):
        def get_field(safe_field_name: str, safe_field_type: str) -> AnnAssign:
            return AnnAssign(
                target=Name(id=safe_field_name, ctx=Store()),
                annotation=Subscript(
                    value=Name(id='Optional', ctx=Load()),
                    slice=Name(id=safe_field_type, ctx=Load()), ctx=Load()
                ), value=Constant(value=None), simple=1
            )

        self._process_field_template(field, fields, get_field)
        self._importer.add_import(
            ImportFrom(module='typing', names=[alias(name='Optional')], level=0), self._pyfile
        )

    def process_field(
        self, field: Field, fields
    ):
        if field.cardinality == FieldCardinality.REPEATED:
            self._process_repeated_field(field, fields)
        elif field.cardinality == FieldCardinality.OPTIONAL:
            self._process_optional_field(field, fields)
        else:
            self._process_single_field(field, fields)

    def _process_field_template(
        self, field: Field, fields: List[ast.stmt],
        get_field: Callable[[str, str], AnnAssign]
    ):
        safe_field_name = self._safe_field_name(field.name)
        field_type = field.type
        try:
            field_type, field_import = self._type_mapper.map(field_type)
            if field_import is not None:
                self._importer.add_import(
                    field_import, self._pyfile
                )
        except ValueError:
            if '.' in field_type:
                class_name = field_type.split('.')[0]
                self._importer.register_dependency(class_name, self._pyfile)
            else:
                self._importer.register_dependency(field_type, self._pyfile)
            field_type = f"'{field_type}'"

        fields.append(
            get_field(safe_field_name, field_type)
        )

    def _process_repeated_field(
        self, field: Field, fields
    ):
        def get_field(safe_field_name: str, safe_field_type: str) -> AnnAssign:
            return AnnAssign(
                target=Name(id=safe_field_name, ctx=Store()),
                annotation=Subscript(
                    value=Name(id='List', ctx=Load()),
                    slice=Name(id=safe_field_type, ctx=Load()), ctx=Load()
                ), simple=1
            )

        self._process_field_template(field, fields, get_field)
        self._importer.add_import(
            ImportFrom(module='typing', names=[alias(name='List')], level=0), self._pyfile
        )

    def _process_single_field(
        self, field: Field, fields
    ):
        def get_field(safe_field_name: str, safe_field_type: str) -> AnnAssign:
            return AnnAssign(
                target=Name(id=safe_field_name, ctx=Store()),
                annotation=Name(id=safe_field_type, ctx=Load()), simple=1
            )

        self._process_field_template(field, fields, get_field)

    def _safe_field_name(self, unsafe_field_name: str) -> str:
        if keyword.iskeyword(unsafe_field_name):
            return f'{unsafe_field_name}_'
        return unsafe_field_name


class ProtoMessageProcessor:
    def __init__(self, importer: Importer, pyfile: Path, type_mapper: TypeMapper):
        self._importer = importer
        self._pyfile = pyfile
        self._type_mapper = type_mapper

    def process_proto_message(self,
        current_element
    ) -> ClassDef:
        class_body = []
        for element in current_element.elements:
            if isinstance(element, Field):
                proto_field_processor = ProtoFieldProcessor(self._importer, self._pyfile, self._type_mapper)
                proto_field_processor.process_field(element, class_body)
            elif isinstance(element, Comment):
                # todo process comments
                continue
            elif isinstance(element, Enum):
                proto_enum_processor = ProtoEnumProcessor(self._importer, self._pyfile)
                class_body.append(
                    proto_enum_processor.process_enum(
                        element
                    )
                )
            elif isinstance(element, OneOf):
                # todo process oneof
                continue
            elif isinstance(element, Message):
                class_body.append(
                    self.process_proto_message(element)
                )
            elif isinstance(element, Reserved):
                continue
            else:
                raise NotImplementedError(f'Unknown element {element}')
        if not class_body:
            class_body.append(Pass())
        self._importer.add_import(
            ImportFrom(module='dataclasses', names=[alias(name='dataclass')], level=0), self._pyfile
        )
        class_name = current_element.name
        class_body = self._reorder_fields(class_body)
        self._importer.register_class(class_name, self._pyfile)
        return ClassDef(
            name=class_name,
            bases=[],
            keywords=[],
            body=class_body,
            decorator_list=[Name(id='dataclass', ctx=Load())]
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


class SourceGenerator:
    def __init__(self, proto_file: Path, out_dir: Path, pyfile: Path, parser: Parser, type_mapper: TypeMapper, importer: Importer):
        self._parser = parser
        self._type_mapper = type_mapper
        self._importer = importer
        self._proto_file = proto_file
        self._out_dir = out_dir
        self._pyfile = pyfile
        self._body: List[ast.stmt] = []
        self._imports: Set[AstImport] = set()

    def generate_source(self) -> Module:
        logger.debug(f'Generating source for {self._proto_file}')
        with open(self._proto_file) as f:
            text = f.read()

        file: File = self._parser.parse(text)

        for element in file.file_elements:
            if isinstance(element, Message):
                proto_message_processor = ProtoMessageProcessor(self._importer, self._pyfile, self._type_mapper)
                self._body.append(proto_message_processor.process_proto_message(element))
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
                proto_enum_processor = ProtoEnumProcessor(
                    self._importer, self._pyfile
                )
                self._body.append(
                    proto_enum_processor.process_enum(element)
                )
            elif isinstance(element, NoneType):
                continue
            elif isinstance(element, Extension):
                continue
            else:
                raise NotImplementedError(f'Unknown element {element}')
        module = Module(
            body=list(self._imports) + self._body, type_ignores=[]
        )

        return module


class Generator:
    def __init__(self, parser: Parser, type_mapper: TypeMapper, importer: Importer):
        self._parser = parser
        self._type_mapper = type_mapper
        self._importer = importer

    def generate_sources(self, proto_dir: Path, out_dir: Path):
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / '__init__.py').touch()
        proto_files = list(proto_dir.rglob('*.proto'))
        modules: Dict[Path, Module] = {}
        for proto_file in proto_files:
            pyfile = proto_file.relative_to(proto_dir).with_suffix('.py')
            logger.debug(pyfile)
            source_generator = SourceGenerator(proto_file, out_dir, pyfile, self._parser, self._type_mapper, self._importer)
            module = source_generator.generate_source()
            modules[proto_file] = module

        self._importer.remove_circular_dependencies()
        for proto_file in proto_files:
            pyfile = proto_file.relative_to(proto_dir).with_suffix('.py')
            imports = self._importer.get_dependency_imports(pyfile)
            module = modules[proto_file]
            self._insert_imports(module, imports)

            result_src = astor.to_source(module)

            (out_dir / pyfile).parent.mkdir(parents=True, exist_ok=True)
            with open(out_dir / pyfile, 'w') as f:
                f.write(result_src)

    def _insert_imports(self, module: Module, imports: Set[AstImport]):
        body_imports = []
        body = []
        for element in module.body:
            if isinstance(element, Import) or isinstance(element, ImportFrom):
                body_imports.append(element)
            else:
                body.append(element)
        body_imports.extend(imports)
        body_imports.sort()
        module.body = body_imports + body


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    parser = Parser()
    type_mapper = TypeMapper()
    importer = Importer()
    gen = Generator(parser, type_mapper, importer)
    gen.generate_sources(
        proto_dir=ROOT_DIR / 'tinkoff/invest/grpc',
        out_dir=ROOT_DIR / 'src' / "models",
    )
