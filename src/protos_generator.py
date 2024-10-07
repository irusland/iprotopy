import subprocess
from pathlib import Path


class ProtosGenerator:
    def generate_protos(self, proto_include_path: Path, models_path: Path):
        models_dir = models_path
        models_dir.mkdir(parents=True, exist_ok=True)

        proto_files = list(proto_include_path.rglob('*.proto'))

        if not proto_files:
            raise ValueError(f'No .proto files found in {proto_include_path}')

        command = [
            'python',
            '-m',
            'grpc_tools.protoc',
            f'--proto_path={proto_include_path}',
            f'--mypy_out={models_path}',
            f'--python_out={models_path}',
            f'--grpc_python_out={models_path}',
        ] + [str(proto) for proto in proto_files]

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            raise ValueError(f'Error while generating protos: {e}') from e


if __name__ == '__main__':
    project_root = Path('..').resolve()
    proto_include_path = project_root / 'protos'
    models_output_path = project_root

    generator = ProtosGenerator()
    generator.generate_protos(proto_include_path, models_output_path)
