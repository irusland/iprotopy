import ast
from ast import *

src = """
from datetime import datetime
"""

ast_src = ast.parse(src)

print(ast.dump(ast_src))
