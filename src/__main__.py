import logging

from paths import ROOT_DIR
from src.package_generator import PackageGenerator

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    gen = PackageGenerator()
    gen.generate_sources(
        proto_dir=ROOT_DIR / 'protos',
        out_dir=ROOT_DIR / 'usage/package',
    )
