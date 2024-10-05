import datetime
from base_service import BaseService
from common import MoneyValue
from common import PriceType
from common import Quotation
from common import ResponseMetadata
from dataclasses import dataclass
from enum import Enum
from typing import List
from typing import Optional


class StopOrdersService(BaseService):
    """/* Сервис предназначен для работы со стоп-заявками:</br> **1**.
                               выставление;</br> **2**. отмена;</br> **3**. получение списка стоп-заявок.*/"""
    _protobuf = stoporders_pb2
    _protobuf_grpc = stoporders_pb2_grpc
    _protobuf_stub = _protobuf_grpc.StopOrdersServiceStub

    def PostStopOrder(self, request: 'PostStopOrderRequest'
        ) ->'PostStopOrderResponse':
        pass

    def GetStopOrders(self, request: 'GetStopOrdersRequest'
        ) ->'GetStopOrdersResponse':
        pass

    def CancelStopOrder(self, request: 'CancelStopOrderRequest'
        ) ->'CancelStopOrderResponse':
        pass


@dataclass
class PostStopOrderRequest:
    quantity: int
    direction: 'StopOrderDirection'
    account_id: str
    expiration_type: 'StopOrderExpirationType'
    stop_order_type: 'StopOrderType'
    instrument_id: str
    exchange_order_type: 'ExchangeOrderType'
    take_profit_type: 'TakeProfitType'
    trailing_data: 'TrailingData'
    price_type: 'PriceType'
    order_id: str
    figi: Optional[str] = None
    price: Optional['Quotation'] = None
    stop_price: Optional['Quotation'] = None
    expire_date: Optional[datetime] = None


    @dataclass
    class TrailingData:
        indent: 'Quotation'
        indent_type: 'TrailingValueType'
        spread: 'Quotation'
        spread_type: 'TrailingValueType'


@dataclass
class PostStopOrderResponse:
    stop_order_id: str
    order_request_id: str
    response_metadata: 'ResponseMetadata'


@dataclass
class GetStopOrdersRequest:
    account_id: str
    status: 'StopOrderStatusOption'
    from_: datetime
    to: datetime


@dataclass
class GetStopOrdersResponse:
    stop_orders: List['StopOrder']


@dataclass
class CancelStopOrderRequest:
    account_id: str
    stop_order_id: str


@dataclass
class CancelStopOrderResponse:
    time: datetime


@dataclass
class StopOrder:
    stop_order_id: str
    lots_requested: int
    figi: str
    direction: 'StopOrderDirection'
    currency: str
    order_type: 'StopOrderType'
    create_date: datetime
    activation_date_time: datetime
    expiration_time: datetime
    price: 'MoneyValue'
    stop_price: 'MoneyValue'
    instrument_uid: str
    take_profit_type: 'TakeProfitType'
    trailing_data: 'TrailingData'
    status: 'StopOrderStatusOption'
    exchange_order_type: 'ExchangeOrderType'


    @dataclass
    class TrailingData:
        indent: 'Quotation'
        indent_type: 'TrailingValueType'
        spread: 'Quotation'
        spread_type: 'TrailingValueType'
        status: 'TrailingStopStatus'
        price: 'Quotation'
        extr: 'Quotation'


class StopOrderDirection(Enum):
    STOP_ORDER_DIRECTION_UNSPECIFIED = 0
    STOP_ORDER_DIRECTION_BUY = 1
    STOP_ORDER_DIRECTION_SELL = 2


class StopOrderExpirationType(Enum):
    STOP_ORDER_EXPIRATION_TYPE_UNSPECIFIED = 0
    STOP_ORDER_EXPIRATION_TYPE_GOOD_TILL_CANCEL = 1
    STOP_ORDER_EXPIRATION_TYPE_GOOD_TILL_DATE = 2


class StopOrderType(Enum):
    STOP_ORDER_TYPE_UNSPECIFIED = 0
    STOP_ORDER_TYPE_TAKE_PROFIT = 1
    STOP_ORDER_TYPE_STOP_LOSS = 2
    STOP_ORDER_TYPE_STOP_LIMIT = 3


class StopOrderStatusOption(Enum):
    STOP_ORDER_STATUS_UNSPECIFIED = 0
    STOP_ORDER_STATUS_ALL = 1
    STOP_ORDER_STATUS_ACTIVE = 2
    STOP_ORDER_STATUS_EXECUTED = 3
    STOP_ORDER_STATUS_CANCELED = 4
    STOP_ORDER_STATUS_EXPIRED = 5


class ExchangeOrderType(Enum):
    EXCHANGE_ORDER_TYPE_UNSPECIFIED = 0
    EXCHANGE_ORDER_TYPE_MARKET = 1
    EXCHANGE_ORDER_TYPE_LIMIT = 2


class TakeProfitType(Enum):
    TAKE_PROFIT_TYPE_UNSPECIFIED = 0
    TAKE_PROFIT_TYPE_REGULAR = 1
    TAKE_PROFIT_TYPE_TRAILING = 2


class TrailingValueType(Enum):
    TRAILING_VALUE_UNSPECIFIED = 0
    TRAILING_VALUE_ABSOLUTE = 1
    TRAILING_VALUE_RELATIVE = 2


class TrailingStopStatus(Enum):
    TRAILING_STOP_UNSPECIFIED = 0
    TRAILING_STOP_ACTIVE = 1
    TRAILING_STOP_ACTIVATED = 2
