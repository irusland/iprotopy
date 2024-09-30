from pprint import pprint

import astor
import ast
from ast import *


src = """
class IndicatorInterval:
    pass

"""

ast_src = ast.parse(src)

print(ast.dump(ast_src))

Module(
    body=[
        ImportFrom(module='typing', names=[alias(name='Optional')], level=0),
          ClassDef(
              name='ClassName', bases=[], keywords=[], body=[
                  AnnAssign(
                    target=Name(id='field1', ctx=Store()),
                    annotation=Name(id='int', ctx=Load()), simple=1
                  ),
                  AnnAssign(
                  target=Name(id='field2', ctx=Store()), annotation=Subscript(
                      value=Name(id='Optional', ctx=Load()),
                      slice=Name(id='bool', ctx=Load()), ctx=Load()
                  ), value=Constant(value=False), simple=1
              )], decorator_list=[]
          )], type_ignores=[]
)
