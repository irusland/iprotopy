import ast
from ast import *

src = """
from models.tinkoff.invest.grpc.common import MoneyValue
"""

ast_src = ast.parse(src)

print(ast.dump(ast_src))
