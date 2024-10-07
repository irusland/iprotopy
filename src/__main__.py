import logging

from proto_schema_parser import Parser

from paths import ROOT_DIR
from src.package_generator import PackageGenerator
from src.protos_generator import ProtosGenerator
from src.type_mapper import TypeMapper

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    parser = Parser()
    type_mapper = TypeMapper()
    protos_generator = ProtosGenerator()
    gen = PackageGenerator(parser, type_mapper, protos_generator)
    gen.generate_sources(
        root_dir=ROOT_DIR,
        proto_dir=ROOT_DIR / 'tinkoff/invest/grpc',
        out_dir=ROOT_DIR / "models",
    )
