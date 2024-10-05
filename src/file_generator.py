import ast
import logging
from _ast import (
    Assign,
    Attribute,
    Call,
    FunctionDef,
    Load,
    Name,
    Pass,
    Store,
    Subscript,
    alias,
    arg,
    arguments,
)
from ast import ClassDef, Constant, Expr, Module
from pathlib import Path
from types import NoneType
from typing import List

from proto_schema_parser import Message, Option, Parser
from proto_schema_parser.ast import (
    Comment,
    Enum,
    Extension,
    File,
    Method,
    Package,
    Service,
)
from proto_schema_parser.ast import (
    Import as ProtoImport,
)

from domestic_importer import DomesticImporter
from enum_generator import EnumGenerator
from importer import Importer
from message_class_generator import MessageClassGenerator
from src.imports import ImportFrom
from type_mapper import TypeMapper

logger = logging.getLogger(__name__)


class ServiceMethodGenerator:
    _unary_input_arg_name = 'request'
    _stream_input_arg_name = f'{_unary_input_arg_name}s'

    def __init__(self, importer: DomesticImporter):
        self._importer = importer

    def process_service_method(self, method: Method) -> FunctionDef:
        input_class = method.input_type.type
        is_input_stream = method.input_type.stream
        output_class = method.output_type.type
        is_output_stream = method.output_type.stream

        args = self._get_args(input_class, is_input_stream)

        output_annotation = self._get_annotation(output_class, is_output_stream)

        return FunctionDef(
            name=method.name,
            args=args,
            body=[Pass()],
            decorator_list=[],
            returns=output_annotation,
        )

    def _get_annotation(self, class_type: str, is_stream: bool) -> ast.expr:
        self._importer.register_dependency(class_type)
        if is_stream:
            self._importer.add_import(
                ImportFrom(module='typing', names=[alias(name='Iterable')], level=0)
            )
            return Subscript(
                value=Name(id='Iterable', ctx=Load()),
                slice=Constant(value=class_type),
                ctx=Load(),
            )
        return Constant(value=class_type)

    def _get_args(self, input_class: str, is_input_stream: bool) -> arguments:
        input_arg_name = (
            self._stream_input_arg_name
            if is_input_stream
            else self._unary_input_arg_name
        )
        input_annotation = self._get_annotation(input_class, is_input_stream)
        return arguments(
            posonlyargs=[],
            args=[
                arg(arg='self'),
                arg(
                    arg=input_arg_name,
                    annotation=input_annotation,
                ),
            ],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[],
        )


class BaseServiceSourceGenerator:
    def __init__(self, importer: DomesticImporter):
        self._importer = importer

    def create_source(self) -> Module:
        class_name = 'BaseService'
        body = [
            ClassDef(
                name=class_name,
                bases=[],
                keywords=[],
                body=[
                    Assign(
                        targets=[Name(id='_protobuf_stub', ctx=Store())],
                        value=Constant(value=None),
                    ),
                    FunctionDef(
                        name='__init__',
                        args=arguments(
                            posonlyargs=[],
                            args=[
                                arg(arg='self'),
                                arg(arg='channel'),
                                arg(arg='metadata'),
                            ],
                            kwonlyargs=[],
                            kw_defaults=[],
                            defaults=[],
                        ),
                        body=[
                            Assign(
                                targets=[
                                    Attribute(
                                        value=Name(id='self', ctx=Load()),
                                        attr='_stub',
                                        ctx=Store(),
                                    )
                                ],
                                value=Call(
                                    func=Attribute(
                                        value=Name(id='self', ctx=Load()),
                                        attr='_protobuf_stub',
                                        ctx=Load(),
                                    ),
                                    args=[Name(id='channel', ctx=Load())],
                                    keywords=[],
                                ),
                            ),
                            Assign(
                                targets=[
                                    Attribute(
                                        value=Name(id='self', ctx=Load()),
                                        attr='_metadata',
                                        ctx=Store(),
                                    )
                                ],
                                value=Name(id='metadata', ctx=Load()),
                            ),
                        ],
                        decorator_list=[],
                    ),
                ],
                decorator_list=[],
            )
        ]
        self._importer.register_class(class_name)
        return Module(body=body, type_ignores=[])


class ServiceGenerator:
    def __init__(self, importer: DomesticImporter, pyfile: Path):
        self._importer = importer
        self._pyfile = pyfile

    def process_service(self, service: Service) -> ClassDef:
        body = []

        self._try_add_docstring(body, service)

        body.extend(self._get_protobuf_attributes(service))

        for element in service.elements:
            if isinstance(element, Comment):
                continue
            elif isinstance(element, Method):
                service_method_generator = ServiceMethodGenerator(self._importer)
                body.append(service_method_generator.process_service_method(element))
                continue
            else:
                raise NotImplementedError(f'Unknown element {element}')

        bases = self._get_bases()
        return ClassDef(
            name=service.name,
            bases=bases,
            keywords=[],
            body=body,
            decorator_list=[],
        )

    def _try_add_docstring(self, body: List[ast.stmt], service: Service):
        if service.elements and isinstance(service.elements[0], Comment):
            body.append(Expr(value=Constant(value=service.elements[0].text)))
            service.elements = service.elements[1:]

    def _get_bases(self) -> List[ast.expr]:
        self._importer.register_dependency('BaseService')
        return [Name(id='BaseService', ctx=Load())]

    def _get_protobuf_attributes(self, service: Service) -> List[ast.stmt]:
        package_name = self._pyfile.stem
        protobuf_package_name = f'{package_name}_pb2'
        protobuf_grpc_package_name = f'{package_name}_pb2_grpc'
        return [
            Assign(
                targets=[Name(id='_protobuf', ctx=Store())],
                value=Name(id=protobuf_package_name, ctx=Load()),
            ),
            Assign(
                targets=[Name(id='_protobuf_grpc', ctx=Store())],
                value=Name(id=protobuf_grpc_package_name, ctx=Load()),
            ),
            Assign(
                targets=[Name(id='_protobuf_stub', ctx=Store())],
                value=Attribute(
                    value=Name(id='_protobuf_grpc', ctx=Load()),
                    attr=f'{service.name}Stub',
                    ctx=Load(),
                ),
            ),
        ]


class SourceGenerator:
    def __init__(
        self,
        proto_file: Path,
        out_dir: Path,
        pyfile: Path,
        parser: Parser,
        type_mapper: TypeMapper,
        global_importer: Importer,
    ):
        self._parser = parser
        self._type_mapper = type_mapper
        self._importer = DomesticImporter(global_importer, pyfile)
        self._proto_file = proto_file
        self._out_dir = out_dir
        self._pyfile = pyfile
        self._body: List[ast.stmt] = []

    def generate_source(self) -> Module:
        logger.debug(f'Generating source for {self._proto_file}')
        with open(self._proto_file) as f:
            text = f.read()

        file: File = self._parser.parse(text)

        for element in file.file_elements:
            if isinstance(element, Message):
                proto_message_processor = MessageClassGenerator(
                    self._importer, self._type_mapper
                )
                self._body.append(
                    proto_message_processor.process_proto_message(element)
                )
            elif isinstance(element, Package):
                continue
            elif isinstance(element, Option):
                continue
            elif isinstance(element, ProtoImport):
                continue
            elif isinstance(element, Service):
                service_generator = ServiceGenerator(self._importer, self._pyfile)
                self._body.append(service_generator.process_service(element))
                # todo AsyncServiceGenerator
            elif isinstance(element, Comment):
                continue
            elif isinstance(element, Enum):
                proto_enum_processor = EnumGenerator(self._importer)
                self._body.append(proto_enum_processor.process_enum(element))
            elif isinstance(element, NoneType):
                continue
            elif isinstance(element, Extension):
                continue
            else:
                raise NotImplementedError(f'Unknown element {element}')
        return Module(body=self._body, type_ignores=[])
