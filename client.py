from datetime import datetime
from pprint import pprint

import grpc

from tinkoff.invest.grpc import users_pb2_grpc, users_pb2
from tinkoff.invest.grpc.users_pb2 import (
    GetAccountsResponse, GetAccountsRequest,
    AccountStatus,
)
from tinkoff.invest.grpc.users_pb2_grpc import UsersServiceStub

creds = grpc.ssl_channel_credentials()

print(creds)

channel = grpc.secure_channel('invest-public-api.tinkoff.ru', creds)

stub = UsersServiceStub(channel)


token = "t.vc2ahqvqQhkMz3yMFmJ9zsmNAchIXGVVXvJILCh51PArAcQ_HBFjsVFl4r_R_clh0jUR2vONSnKrxYOIMusY-A"



from dataclasses import dataclass
from io import BytesIO

from pure_protobuf.annotations import Field
from pure_protobuf.message import BaseMessage
from typing_extensions import Annotated


@dataclass
class GetAccountsRequest(BaseMessage):
    pass


request = GetAccountsRequest()
buffer = bytes(request)
print(buffer)
assert buffer == b''
assert GetAccountsRequest.read_from(BytesIO(buffer)) == request


request = GetAccountsRequest()

response: GetAccountsResponse = stub.GetAccounts(request, metadata=[("authorization", f"Bearer {token}")])


pprint(response.accounts[0].opened_date)

import grpc
from grpc_interceptor import ClientCallDetails, ClientInterceptor


class BearerTokenInterceptor(ClientInterceptor):
    def __init__(self, token):
        self.token = token

    def intercept_call(
        self, client_call_details: ClientCallDetails, request_iterator,
        request_streaming, response_streaming
    ):
        new_metadata = []
        if client_call_details.metadata is not None:
            new_metadata = list(client_call_details.metadata)
        new_metadata.append(('authorization', f'Bearer {self.token}'))

        new_client_call_details = ClientCallDetails(
            client_call_details.method, client_call_details.timeout, new_metadata,
            client_call_details.credentials, client_call_details.wait_for_ready,
            client_call_details.compression
        )
        return new_client_call_details, request_iterator, client_call_details


# Usage
token = 'YOUR_ACCESS_TOKEN'
interceptor = BearerTokenInterceptor(token)
channel = grpc.intercept_channel(grpc.insecure_channel('localhost:50051'), interceptor)
stub = users_pb2_grpc.UsersServiceStub(channel)

# Now every call made with this stub will include the bearer token in the metadata
try:
    response = stub.GetAccounts(users_pb2.GetAccountsRequest())
    print(response)
except grpc.RpcError as e:
    print(f"RPC failed: {e.code()} {e.details()}")



