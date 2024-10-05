from pathlib import Path
from typing import Set

from importer import Importer
from src.import_types import AstImport


class DomesticImporter:
    def __init__(self, importer: Importer, pyfile: Path):
        self._importer = importer
        self._pyfile = pyfile

    def register_class(self, class_name: str):
        self._importer.register_class(class_name, self._pyfile)

    def register_dependency(self, class_name: str):
        self._importer.register_dependency(class_name, self._pyfile)

    def get_dependency_imports(self) -> Set[AstImport]:
        return self._importer.get_dependency_imports(self._pyfile)

    def add_import(self, import_statement: AstImport):
        self._importer.add_import(import_statement, self._pyfile)
