import ast
from ast import *

src = """
from mypy_models.tinkoff.invest.grpc import users_pb2, users_pb2_grpc
from src.convertion import dataclass_to_protobuff, protobuf_to_dataclass


class BaseService:
    _protobuf_stub = None

    def __init__(self, channel, metadata):
        self._stub = self._protobuf_stub(channel)
        self._metadata = metadata


class UsersService(BaseService):

    _protobuf = users_pb2
    _protobuf_grpc = users_pb2_grpc
    _protobuf_stub = _protobuf_grpc.UsersServiceStub
    
    def GetAccounts(self, request: 'GetAccountsRequest') -> 'GetAccountsResponse':
        protobuff_request = dataclass_to_protobuff(
            request, self._protobuf.GetAccountsRequest()
        )
        response, call = self._stub.GetAccounts.with_call(
            request=protobuff_request,
            metadata=self._metadata,
        )
        return protobuf_to_dataclass(response, GetAccountsResponse)

"""

ast_src = ast.parse(src)

print(ast.dump(ast_src))

Module(
    body=[ImportFrom(
        module='mypy_models.tinkoff.invest.grpc',
        names=[alias(name='users_pb2'), alias(name='users_pb2_grpc')], level=0
    ), ImportFrom(
        module='src.convertion', names=[alias(name='dataclass_to_protobuff'),
                                        alias(name='protobuf_to_dataclass')], level=0
    ), ClassDef(
        name='BaseService', bases=[], keywords=[], body=[Assign(
            targets=[Name(id='_protobuf_stub', ctx=Store())], value=Constant(value=None)
        ), FunctionDef(
            name='__init__', args=arguments(
                posonlyargs=[],
                args=[arg(arg='self'), arg(arg='channel'), arg(arg='metadata')],
                kwonlyargs=[], kw_defaults=[], defaults=[]
            ), body=[Assign(
                targets=[Attribute(
                    value=Name(id='self', ctx=Load()), attr='_stub', ctx=Store()
                )], value=Call(
                    func=Attribute(
                        value=Name(id='self', ctx=Load()), attr='_protobuf_stub',
                        ctx=Load()
                    ), args=[Name(id='channel', ctx=Load())], keywords=[]
                )
            ), Assign(
                targets=[Attribute(
                    value=Name(id='self', ctx=Load()), attr='_metadata', ctx=Store()
                )], value=Name(id='metadata', ctx=Load())
            )], decorator_list=[]
        )], decorator_list=[]
    ),


    ClassDef(
        name='UsersService', bases=[Name(id='BaseService', ctx=Load())], keywords=[],
        body=[Assign(
            targets=[Name(id='_protobuf', ctx=Store())],
            value=Name(id='users_pb2', ctx=Load())
        ), Assign(
            targets=[Name(id='_protobuf_grpc', ctx=Store())],
            value=Name(id='users_pb2_grpc', ctx=Load())
        ), Assign(
            targets=[Name(id='_protobuf_stub', ctx=Store())], value=Attribute(
                value=Name(id='_protobuf_grpc', ctx=Load()), attr='UsersServiceStub',
                ctx=Load()
            )
        ),

            FunctionDef(
            name='GetAccounts', args=arguments(
                posonlyargs=[], args=[arg(arg='self'), arg(
                    arg='request', annotation=Constant(value='GetAccountsRequest')
                )], kwonlyargs=[], kw_defaults=[], defaults=[]
            ), body=[Assign(
                targets=[Name(id='protobuff_request', ctx=Store())], value=Call(
                    func=Name(id='dataclass_to_protobuff', ctx=Load()),
                    args=[Name(id='request', ctx=Load()), Call(
                        func=Attribute(
                            value=Attribute(
                                value=Name(id='self', ctx=Load()), attr='_protobuf',
                                ctx=Load()
                            ), attr='GetAccountsRequest', ctx=Load()
                        ), args=[], keywords=[]
                    )], keywords=[]
                )
            ), Assign(
                targets=[Tuple(
                    elts=[Name(id='response', ctx=Store()),
                          Name(id='call', ctx=Store())], ctx=Store()
                )], value=Call(
                    func=Attribute(
                        value=Attribute(
                            value=Attribute(
                                value=Name(id='self', ctx=Load()), attr='_stub',
                                ctx=Load()
                            ), attr='GetAccounts', ctx=Load()
                        ), attr='with_call', ctx=Load()
                    ), args=[], keywords=[keyword(
                        arg='request', value=Name(id='protobuff_request', ctx=Load())
                    ), keyword(
                        arg='metadata', value=Attribute(
                            value=Name(id='self', ctx=Load()), attr='_metadata',
                            ctx=Load()
                        )
                    )]
                )
            ), Return(
                value=Call(
                    func=Name(id='protobuf_to_dataclass', ctx=Load()),
                    args=[Name(id='response', ctx=Load()),
                          Name(id='GetAccountsResponse', ctx=Load())], keywords=[]
                )
            )], decorator_list=[], returns=Constant(value='GetAccountsResponse')
        )], decorator_list=[]
    )], type_ignores=[]
)
