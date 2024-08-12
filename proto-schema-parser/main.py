import astor
from proto_schema_parser.ast import File, Message, Field, MessageElement
from proto_schema_parser.parser import Parser

from paths import ROOT_DIR
from ast import *


with open(ROOT_DIR / 'tinkoff/invest/grpc' / 'marketdata.proto') as f:
    text = f.read()

result: File = Parser().parse(text)


body = []

for element in result.file_elements:
    # print(element)
    if isinstance(element, Message):
        print(element)
        fields = []
        for field in element.elements:
            if not isinstance(field, Field):
                continue
            fields.append(
                AnnAssign(
                    target=Name(id=field.name, ctx=Store()),
                    annotation=Name(id=field.type, ctx=Load()), simple=1
                )
            )

        body.append(
            ClassDef(
                name=element.name,
                bases=[],
                keywords=[],
                body=fields,
                decorator_list=[]
            )
        )


module = Module(
    body=body + [
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
          )
    ], type_ignores=[]
)


result_src = astor.to_source(module)

# print(result_src)

with open(ROOT_DIR / 'proto-schema-parser' / 'result.py', 'w') as f:
    f.write(result_src)


