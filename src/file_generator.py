import ast
import logging
from _ast import Module
from pathlib import Path
from types import NoneType
from typing import List

from proto_schema_parser import Parser, Message, Option
from proto_schema_parser.ast import (
    File, Package, Import as ProtoImport, Service,
    Comment, Enum, Extension,
)
from type_mapper import TypeMapper
from importer import Importer
from domestic_importer import DomesticImporter
from enum_generator import ProtoEnumProcessor
from message_class_generator import ProtoMessageProcessor

logger = logging.getLogger(__name__)

class SourceGenerator:
    def __init__(
        self, proto_file: Path, out_dir: Path, pyfile: Path, parser: Parser,
        type_mapper: TypeMapper, global_importer: Importer
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
                proto_message_processor = ProtoMessageProcessor(
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
                # todo process services
                continue
            elif isinstance(element, Comment):
                continue
            elif isinstance(element, Enum):
                proto_enum_processor = ProtoEnumProcessor(
                    self._importer
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
        module = Module(body=self._body, type_ignores=[])

        return module
