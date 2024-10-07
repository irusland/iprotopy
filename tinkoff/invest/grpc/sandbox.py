from base_service import BaseService
from dataclasses import dataclass
from src.convertion import dataclass_to_protobuf
from src.convertion import protobuf_to_dataclass
from tinkoff.invest.grpc.common import MoneyValue
from tinkoff.invest.grpc.operations import GetOperationsByCursorRequest
from tinkoff.invest.grpc.operations import GetOperationsByCursorResponse
from tinkoff.invest.grpc.operations import OperationsRequest
from tinkoff.invest.grpc.operations import OperationsResponse
from tinkoff.invest.grpc.operations import PortfolioRequest
from tinkoff.invest.grpc.operations import PortfolioResponse
from tinkoff.invest.grpc.operations import PositionsRequest
from tinkoff.invest.grpc.operations import PositionsResponse
from tinkoff.invest.grpc.operations import WithdrawLimitsRequest
from tinkoff.invest.grpc.operations import WithdrawLimitsResponse
from tinkoff.invest.grpc.orders import CancelOrderRequest
from tinkoff.invest.grpc.orders import CancelOrderResponse
from tinkoff.invest.grpc.orders import GetMaxLotsRequest
from tinkoff.invest.grpc.orders import GetMaxLotsResponse
from tinkoff.invest.grpc.orders import GetOrderStateRequest
from tinkoff.invest.grpc.orders import GetOrdersRequest
from tinkoff.invest.grpc.orders import GetOrdersResponse
from tinkoff.invest.grpc.orders import OrderState
from tinkoff.invest.grpc.orders import PostOrderRequest
from tinkoff.invest.grpc.orders import PostOrderResponse
from tinkoff.invest.grpc.orders import ReplaceOrderRequest
from tinkoff.invest.grpc.users import GetAccountsRequest
from tinkoff.invest.grpc.users import GetAccountsResponse
from typing import Optional


class SandboxService(BaseService):
    """// Методы для работы с песочницей Tinkoff Invest API"""
    _protobuf = sandbox_pb2
    _protobuf_grpc = sandbox_pb2_grpc
    _protobuf_stub = _protobuf_grpc.SandboxServiceStub

    def OpenSandboxAccount(self, request: 'OpenSandboxAccountRequest'
        ) ->'OpenSandboxAccountResponse':
        protobuf_request = dataclass_to_protobuf(request, self._protobuf.
            GetAccountsRequest())
        response, call = self._stub.GetAccounts.with_call(request=
            protobuf_request, metadata=self._metadata)
        return protobuf_to_dataclass(response, GetAccountsResponse)

    def GetSandboxAccounts(self, request: 'GetAccountsRequest'
        ) ->'GetAccountsResponse':
        protobuf_request = dataclass_to_protobuf(request, self._protobuf.
            GetAccountsRequest())
        response, call = self._stub.GetAccounts.with_call(request=
            protobuf_request, metadata=self._metadata)
        return protobuf_to_dataclass(response, GetAccountsResponse)

    def CloseSandboxAccount(self, request: 'CloseSandboxAccountRequest'
        ) ->'CloseSandboxAccountResponse':
        protobuf_request = dataclass_to_protobuf(request, self._protobuf.
            GetAccountsRequest())
        response, call = self._stub.GetAccounts.with_call(request=
            protobuf_request, metadata=self._metadata)
        return protobuf_to_dataclass(response, GetAccountsResponse)

    def PostSandboxOrder(self, request: 'PostOrderRequest'
        ) ->'PostOrderResponse':
        protobuf_request = dataclass_to_protobuf(request, self._protobuf.
            GetAccountsRequest())
        response, call = self._stub.GetAccounts.with_call(request=
            protobuf_request, metadata=self._metadata)
        return protobuf_to_dataclass(response, GetAccountsResponse)

    def ReplaceSandboxOrder(self, request: 'ReplaceOrderRequest'
        ) ->'PostOrderResponse':
        protobuf_request = dataclass_to_protobuf(request, self._protobuf.
            GetAccountsRequest())
        response, call = self._stub.GetAccounts.with_call(request=
            protobuf_request, metadata=self._metadata)
        return protobuf_to_dataclass(response, GetAccountsResponse)

    def GetSandboxOrders(self, request: 'GetOrdersRequest'
        ) ->'GetOrdersResponse':
        protobuf_request = dataclass_to_protobuf(request, self._protobuf.
            GetAccountsRequest())
        response, call = self._stub.GetAccounts.with_call(request=
            protobuf_request, metadata=self._metadata)
        return protobuf_to_dataclass(response, GetAccountsResponse)

    def CancelSandboxOrder(self, request: 'CancelOrderRequest'
        ) ->'CancelOrderResponse':
        protobuf_request = dataclass_to_protobuf(request, self._protobuf.
            GetAccountsRequest())
        response, call = self._stub.GetAccounts.with_call(request=
            protobuf_request, metadata=self._metadata)
        return protobuf_to_dataclass(response, GetAccountsResponse)

    def GetSandboxOrderState(self, request: 'GetOrderStateRequest'
        ) ->'OrderState':
        protobuf_request = dataclass_to_protobuf(request, self._protobuf.
            GetAccountsRequest())
        response, call = self._stub.GetAccounts.with_call(request=
            protobuf_request, metadata=self._metadata)
        return protobuf_to_dataclass(response, GetAccountsResponse)

    def GetSandboxPositions(self, request: 'PositionsRequest'
        ) ->'PositionsResponse':
        protobuf_request = dataclass_to_protobuf(request, self._protobuf.
            GetAccountsRequest())
        response, call = self._stub.GetAccounts.with_call(request=
            protobuf_request, metadata=self._metadata)
        return protobuf_to_dataclass(response, GetAccountsResponse)

    def GetSandboxOperations(self, request: 'OperationsRequest'
        ) ->'OperationsResponse':
        protobuf_request = dataclass_to_protobuf(request, self._protobuf.
            GetAccountsRequest())
        response, call = self._stub.GetAccounts.with_call(request=
            protobuf_request, metadata=self._metadata)
        return protobuf_to_dataclass(response, GetAccountsResponse)

    def GetSandboxOperationsByCursor(self, request:
        'GetOperationsByCursorRequest') ->'GetOperationsByCursorResponse':
        protobuf_request = dataclass_to_protobuf(request, self._protobuf.
            GetAccountsRequest())
        response, call = self._stub.GetAccounts.with_call(request=
            protobuf_request, metadata=self._metadata)
        return protobuf_to_dataclass(response, GetAccountsResponse)

    def GetSandboxPortfolio(self, request: 'PortfolioRequest'
        ) ->'PortfolioResponse':
        protobuf_request = dataclass_to_protobuf(request, self._protobuf.
            GetAccountsRequest())
        response, call = self._stub.GetAccounts.with_call(request=
            protobuf_request, metadata=self._metadata)
        return protobuf_to_dataclass(response, GetAccountsResponse)

    def SandboxPayIn(self, request: 'SandboxPayInRequest'
        ) ->'SandboxPayInResponse':
        protobuf_request = dataclass_to_protobuf(request, self._protobuf.
            GetAccountsRequest())
        response, call = self._stub.GetAccounts.with_call(request=
            protobuf_request, metadata=self._metadata)
        return protobuf_to_dataclass(response, GetAccountsResponse)

    def GetSandboxWithdrawLimits(self, request: 'WithdrawLimitsRequest'
        ) ->'WithdrawLimitsResponse':
        protobuf_request = dataclass_to_protobuf(request, self._protobuf.
            GetAccountsRequest())
        response, call = self._stub.GetAccounts.with_call(request=
            protobuf_request, metadata=self._metadata)
        return protobuf_to_dataclass(response, GetAccountsResponse)

    def GetSandboxMaxLots(self, request: 'GetMaxLotsRequest'
        ) ->'GetMaxLotsResponse':
        protobuf_request = dataclass_to_protobuf(request, self._protobuf.
            GetAccountsRequest())
        response, call = self._stub.GetAccounts.with_call(request=
            protobuf_request, metadata=self._metadata)
        return protobuf_to_dataclass(response, GetAccountsResponse)


@dataclass
class OpenSandboxAccountRequest:
    name: Optional[str] = None


@dataclass
class OpenSandboxAccountResponse:
    account_id: str


@dataclass
class CloseSandboxAccountRequest:
    account_id: str


@dataclass
class CloseSandboxAccountResponse:
    pass


@dataclass
class SandboxPayInRequest:
    account_id: str
    amount: 'MoneyValue'


@dataclass
class SandboxPayInResponse:
    balance: 'MoneyValue'
