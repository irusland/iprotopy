import ast
from ast import *

src = """
class A:
    def method():
        for response in self.stub.TradesStream(
            request=_grpc_helpers.dataclass_to_protobuff(
                request, orders_pb2.TradesStreamRequest()
            ),
            metadata=self.metadata,
        ):
            yield _grpc_helpers.protobuf_to_dataclass(response, TradesStreamResponse)

"""

ast_src = ast.parse(src)

print(ast.dump(ast_src))


