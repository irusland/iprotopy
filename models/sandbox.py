from base_service import BaseService
from common import MoneyValue
from dataclasses import dataclass
from operations import GetOperationsByCursorRequest
from operations import GetOperationsByCursorResponse
from operations import OperationsRequest
from operations import OperationsResponse
from operations import PortfolioRequest
from operations import PortfolioResponse
from operations import PositionsRequest
from operations import PositionsResponse
from operations import WithdrawLimitsRequest
from operations import WithdrawLimitsResponse
from orders import CancelOrderRequest
from orders import CancelOrderResponse
from orders import GetMaxLotsRequest
from orders import GetMaxLotsResponse
from orders import GetOrderStateRequest
from orders import GetOrdersRequest
from orders import GetOrdersResponse
from orders import OrderState
from orders import PostOrderRequest
from orders import PostOrderResponse
from orders import ReplaceOrderRequest
from src.convertion import dataclass_to_protobuf
from src.convertion import protobuf_to_dataclass
from typing import Optional
from users import GetAccountsRequest
from users import GetAccountsResponse


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
