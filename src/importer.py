import logging
from _ast import alias
from pathlib import Path
from typing import Dict, Set

from imports import ImportFrom
from src.import_types import AstImport

logger = logging.getLogger(__name__)


class Importer:
    def __init__(self):
        self._definitions: Dict[str, Path] = {}
        self._dependencies: Dict[Path, Set[str]] = {}
        self._default_dependencies = set(i.__name__ for i in (int, str, bool))
        self._imports: Dict[Path, Set[AstImport]] = {}

    def define_dependency(self, name: str, pyfile: Path):
        if name in self._definitions:
            logger.warning('Class %s already registered', name)
        self._definitions[name] = pyfile

    def import_dependency(self, name: str, pyfile: Path):
        if name in self._default_dependencies:
            return
        dependencies = self._dependencies.get(pyfile, set())
        dependencies.add(name)
        self._dependencies[pyfile] = dependencies

    def get_imports(self, pyfile: Path) -> Set[AstImport]:
        dependencies_imports = {
            self._get_import_for(class_name, pyfile)
            for class_name in self._dependencies.get(pyfile, ())
        }
        for import_ in self._imports.get(pyfile, ()):
            dependencies_imports.add(import_)
        return dependencies_imports

    def _get_import_for(self, class_name: str, pyfile: Path) -> AstImport:
        if class_name not in self._definitions:
            raise ValueError(
                f'Class {class_name} not registered but needed in {pyfile}'
            )
        return ImportFrom(
            module=self._definitions[class_name].stem,
            names=[alias(name=class_name)],
            level=0,
        )

    def remove_circular_dependencies(self):
        for class_name, pyfile in self._definitions.items():
            dependencies = self._dependencies.get(pyfile, set())

            if class_name in dependencies:
                dependencies.remove(class_name)

    def add_import(self, import_statement: AstImport, pyfile: Path):
        imports = self._imports.get(pyfile, set())
        imports.add(import_statement)
        self._imports[pyfile] = imports
