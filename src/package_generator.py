import logging
from _ast import (
    Module,
)
from ast import (
    Module,
)
from pathlib import Path
from typing import Set, Dict

import astor
from proto_schema_parser.parser import Parser

from paths import ROOT_DIR
from file_generator import SourceGenerator
from importer import Importer
from imports import Import, ImportFrom
from src.import_types import AstImport
from type_mapper import TypeMapper

logger = logging.getLogger(__name__)


class PackageGenerator:
    def __init__(self, parser: Parser, type_mapper: TypeMapper):
        self._parser = parser
        self._type_mapper = type_mapper

    def generate_sources(self, proto_dir: Path, out_dir: Path):
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / '__init__.py').touch()
        proto_files = list(proto_dir.rglob('*.proto'))
        modules: Dict[Path, Module] = {}
        importer = Importer()

        for proto_file in proto_files:
            pyfile = proto_file.relative_to(proto_dir).with_suffix('.py')
            logger.debug(pyfile)
            source_generator = SourceGenerator(
                proto_file, out_dir, pyfile, self._parser, self._type_mapper,
                importer
            )
            module = source_generator.generate_source()
            modules[proto_file] = module

        importer.remove_circular_dependencies()

        for proto_file in proto_files:
            pyfile = proto_file.relative_to(proto_dir).with_suffix('.py')
            imports = importer.get_dependency_imports(pyfile)
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
    gen = PackageGenerator(parser, type_mapper)
    gen.generate_sources(
        proto_dir=ROOT_DIR / 'tinkoff/invest/grpc',
        out_dir=ROOT_DIR / "models",
    )
