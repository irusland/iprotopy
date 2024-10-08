import logging

from paths import ROOT_DIR
from src.package_generator import PackageGenerator

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    gen = PackageGenerator()
    usage_dir = ROOT_DIR / 'usage'
    gen.generate_sources(
        proto_dir=usage_dir / 'protos',
        out_dir=usage_dir / 'package',
    )
