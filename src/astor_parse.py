import ast
from ast import *

src = """
from typing import Iterable
class OrdersStreamService:
    def GetOrderState(self, request: 'GetOrderStateRequest') -> Iterable['OrderState']:
        pass

"""

ast_src = ast.parse(src)

print(ast.dump(ast_src))
