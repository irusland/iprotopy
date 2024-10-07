import ast
from _ast import (
    Assign,
    Attribute,
    Call,
    Constant,
    FunctionDef,
    Load,
    Name,
    Return,
    Store,
    Subscript,
    Tuple,
    alias,
    arg,
    arguments,
    keyword,
)

from proto_schema_parser.ast import Method

from constants import SOURCE_DIR_NAME
from src.domestic_importer import DomesticImporter
from src.imports import ImportFrom


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
        body = self._get_function_body(method)
        return FunctionDef(
            name=method.name,
            args=args,
            body=body,
            decorator_list=[],
            returns=output_annotation,
        )

    def _get_annotation(self, class_type: str, is_stream: bool) -> ast.expr:
        self._importer.import_dependency(class_type)
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

    def _get_function_body(self, method: Method) -> list[ast.stmt]:
        method_name = method.name
        request_class_name = method.input_type.type
        response_class_name = method.output_type.type
        body = [
            Assign(
                targets=[Name(id='protobuf_request', ctx=Store())],
                value=Call(
                    func=Name(id='dataclass_to_protobuf', ctx=Load()),
                    args=[
                        Name(id='request', ctx=Load()),
                        Call(
                            func=Attribute(
                                value=Attribute(
                                    value=Name(id='self', ctx=Load()),
                                    attr='_protobuf',
                                    ctx=Load(),
                                ),
                                attr=request_class_name,
                                ctx=Load(),
                            ),
                            args=[],
                            keywords=[],
                        ),
                    ],
                    keywords=[],
                ),
            ),
            Assign(
                targets=[
                    Tuple(
                        elts=[
                            Name(id='response', ctx=Store()),
                            Name(id='call', ctx=Store()),
                        ],
                        ctx=Store(),
                    )
                ],
                value=Call(
                    func=Attribute(
                        value=Attribute(
                            value=Attribute(
                                value=Name(id='self', ctx=Load()),
                                attr='_stub',
                                ctx=Load(),
                            ),
                            attr=method_name,
                            ctx=Load(),
                        ),
                        attr='with_call',
                        ctx=Load(),
                    ),
                    args=[],
                    keywords=[
                        keyword(
                            arg='request',
                            value=Name(id='protobuf_request', ctx=Load()),
                        ),
                        keyword(
                            arg='metadata',
                            value=Attribute(
                                value=Name(id='self', ctx=Load()),
                                attr='_metadata',
                                ctx=Load(),
                            ),
                        ),
                    ],
                ),
            ),
            Return(
                value=Call(
                    func=Name(id='protobuf_to_dataclass', ctx=Load()),
                    args=[
                        Name(id='response', ctx=Load()),
                        Name(id=response_class_name, ctx=Load()),
                    ],
                    keywords=[],
                )
            ),
        ]

        self._importer.add_import(
            ImportFrom(
                module=f'{SOURCE_DIR_NAME}.convertion',
                names=[alias(name='dataclass_to_protobuf')],
                level=0,
            )
        )
        self._importer.add_import(
            ImportFrom(
                module=f'{SOURCE_DIR_NAME}.convertion',
                names=[alias(name='protobuf_to_dataclass')],
                level=0,
            )
        )
        return body
