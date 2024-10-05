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
from typing import Optional
from users import GetAccountsRequest
from users import GetAccountsResponse


class SandboxService:
    """// Методы для работы с песочницей Tinkoff Invest API"""

    def OpenSandboxAccount(self, request: 'OpenSandboxAccountRequest'
        ) ->'OpenSandboxAccountResponse':
        pass

    def GetSandboxAccounts(self, request: 'GetAccountsRequest'
        ) ->'GetAccountsResponse':
        pass

    def CloseSandboxAccount(self, request: 'CloseSandboxAccountRequest'
        ) ->'CloseSandboxAccountResponse':
        pass

    def PostSandboxOrder(self, request: 'PostOrderRequest'
        ) ->'PostOrderResponse':
        pass

    def ReplaceSandboxOrder(self, request: 'ReplaceOrderRequest'
        ) ->'PostOrderResponse':
        pass

    def GetSandboxOrders(self, request: 'GetOrdersRequest'
        ) ->'GetOrdersResponse':
        pass

    def CancelSandboxOrder(self, request: 'CancelOrderRequest'
        ) ->'CancelOrderResponse':
        pass

    def GetSandboxOrderState(self, request: 'GetOrderStateRequest'
        ) ->'OrderState':
        pass

    def GetSandboxPositions(self, request: 'PositionsRequest'
        ) ->'PositionsResponse':
        pass

    def GetSandboxOperations(self, request: 'OperationsRequest'
        ) ->'OperationsResponse':
        pass

    def GetSandboxOperationsByCursor(self, request:
        'GetOperationsByCursorRequest') ->'GetOperationsByCursorResponse':
        pass

    def GetSandboxPortfolio(self, request: 'PortfolioRequest'
        ) ->'PortfolioResponse':
        pass

    def SandboxPayIn(self, request: 'SandboxPayInRequest'
        ) ->'SandboxPayInResponse':
        pass

    def GetSandboxWithdrawLimits(self, request: 'WithdrawLimitsRequest'
        ) ->'WithdrawLimitsResponse':
        pass

    def GetSandboxMaxLots(self, request: 'GetMaxLotsRequest'
        ) ->'GetMaxLotsResponse':
        pass


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
