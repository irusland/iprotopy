import subprocess
from pathlib import Path


class ProtosGenerator:
    def generate_protos(
        self, project_root: Path, proto_include_path: Path, models_path: Path
    ):
        models_dir = models_path
        models_dir.mkdir(parents=True, exist_ok=True)

        proto_files = list(proto_include_path.rglob('*.proto'))

        if not proto_files:
            raise ValueError(f'No .proto files found in {proto_include_path}')

        command = [
            'python',
            '-m',
            'grpc_tools.protoc',
            f'--proto_path={project_root}',
            f'--mypy_out={models_path}',
            f'--python_out={models_path}',
            f'--grpc_python_out={models_path}',
        ] + [str(proto) for proto in proto_files]

        subprocess.run(command, check=True)


if __name__ == '__main__':
    project_root = Path('..')
    proto_include_path = project_root / 'tinkoff/invest/grpc'
    models_output_path = project_root / 'models'
    generator = ProtosGenerator()
    generator.generate_protos(project_root, proto_include_path, models_output_path)
