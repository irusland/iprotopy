import datetime
from common import ErrorDetail
from common import MoneyValue
from common import PriceType
from common import Quotation
from common import ResponseMetadata
from common import ResultSubscriptionStatus
from dataclasses import dataclass
from enum import Enum
from typing import List


@dataclass
class TradesStreamRequest:
    accounts: List[str]


@dataclass
class TradesStreamResponse:
    pass


@dataclass
class OrderTrades:
    order_id: str
    created_at: datetime
    direction: 'OrderDirection'
    figi: str
    trades: List['OrderTrade']
    account_id: str
    instrument_uid: str


@dataclass
class OrderTrade:
    date_time: datetime
    price: 'Quotation'
    quantity: int
    trade_id: str


@dataclass
class PostOrderRequest:
    figi: str
    quantity: int
    price: 'Quotation'
    direction: 'OrderDirection'
    account_id: str
    order_type: 'OrderType'
    order_id: str
    instrument_id: str
    time_in_force: 'TimeInForceType'
    price_type: 'PriceType'


@dataclass
class PostOrderResponse:
    order_id: str
    execution_report_status: 'OrderExecutionReportStatus'
    lots_requested: int
    lots_executed: int
    initial_order_price: 'MoneyValue'
    executed_order_price: 'MoneyValue'
    total_order_amount: 'MoneyValue'
    initial_commission: 'MoneyValue'
    executed_commission: 'MoneyValue'
    aci_value: 'MoneyValue'
    figi: str
    direction: 'OrderDirection'
    initial_security_price: 'MoneyValue'
    order_type: 'OrderType'
    message: str
    initial_order_price_pt: 'Quotation'
    instrument_uid: str
    order_request_id: str
    response_metadata: 'ResponseMetadata'


@dataclass
class CancelOrderRequest:
    account_id: str
    order_id: str


@dataclass
class CancelOrderResponse:
    time: datetime
    response_metadata: 'ResponseMetadata'


@dataclass
class GetOrderStateRequest:
    account_id: str
    order_id: str
    price_type: 'PriceType'


@dataclass
class GetOrdersRequest:
    account_id: str


@dataclass
class GetOrdersResponse:
    orders: List['OrderState']


@dataclass
class OrderState:
    order_id: str
    execution_report_status: 'OrderExecutionReportStatus'
    lots_requested: int
    lots_executed: int
    initial_order_price: 'MoneyValue'
    executed_order_price: 'MoneyValue'
    total_order_amount: 'MoneyValue'
    average_position_price: 'MoneyValue'
    initial_commission: 'MoneyValue'
    executed_commission: 'MoneyValue'
    figi: str
    direction: 'OrderDirection'
    initial_security_price: 'MoneyValue'
    stages: List['OrderStage']
    service_commission: 'MoneyValue'
    currency: str
    order_type: 'OrderType'
    order_date: datetime
    instrument_uid: str
    order_request_id: str


@dataclass
class OrderStage:
    price: 'MoneyValue'
    quantity: int
    trade_id: str
    execution_time: datetime


@dataclass
class ReplaceOrderRequest:
    account_id: str
    order_id: str
    idempotency_key: str
    quantity: int
    price: 'Quotation'
    price_type: 'PriceType'


@dataclass
class GetMaxLotsRequest:
    account_id: str
    instrument_id: str
    price: 'Quotation'


@dataclass
class GetMaxLotsResponse:
    currency: str
    buy_limits: 'BuyLimitsView'
    buy_margin_limits: 'BuyLimitsView'
    sell_limits: 'SellLimitsView'
    sell_margin_limits: 'SellLimitsView'


    @dataclass
    class BuyLimitsView:
        buy_money_amount: 'Quotation'
        buy_max_lots: int
        buy_max_market_lots: int


    @dataclass
    class SellLimitsView:
        sell_max_lots: int


@dataclass
class GetOrderPriceRequest:
    account_id: str
    instrument_id: str
    price: 'Quotation'
    direction: 'OrderDirection'
    quantity: int


@dataclass
class GetOrderPriceResponse:
    total_order_amount: 'MoneyValue'
    initial_order_amount: 'MoneyValue'
    lots_requested: int
    executed_commission: 'MoneyValue'
    executed_commission_rub: 'MoneyValue'
    service_commission: 'MoneyValue'
    deal_commission: 'MoneyValue'


    @dataclass
    class ExtraBond:
        aci_value: 'MoneyValue'
        nominal_conversion_rate: 'Quotation'


    @dataclass
    class ExtraFuture:
        initial_margin: 'MoneyValue'


@dataclass
class OrderStateStreamRequest:
    accounts: List[str]
    ping_delay_millis: int


@dataclass
class OrderStateStreamResponse:


    @dataclass
    class SubscriptionResponse:
        tracking_id: str
        status: 'ResultSubscriptionStatus'
        stream_id: str
        accounts: List[str]
        error: 'ErrorDetail'


    @dataclass
    class OrderState:
        order_id: str
        order_request_id: str
        client_code: str
        created_at: datetime
        execution_report_status: 'OrderExecutionReportStatus'
        status_info: 'StatusCauseInfo'
        ticker: str
        class_code: str
        lot_size: int
        direction: 'OrderDirection'
        time_in_force: 'TimeInForceType'
        order_type: 'OrderType'
        account_id: str
        initial_order_price: 'MoneyValue'
        order_price: 'MoneyValue'
        amount: 'MoneyValue'
        executed_order_price: 'MoneyValue'
        currency: str
        lots_requested: int
        lots_executed: int
        lots_left: int
        lots_cancelled: int
        marker: 'MarkerType'
        trades: List['OrderTrade']
        completion_time: datetime
        exchange: str
        instrument_uid: str


    class MarkerType(Enum):
        MARKER_UNKNOWN = 0
        MARKER_BROKER = 1
        MARKER_CHAT = 2
        MARKER_PAPER = 3
        MARKER_MARGIN = 4
        MARKER_TKBNM = 5
        MARKER_SHORT = 6
        MARKER_SPECMM = 7
        MARKER_PO = 8


    class StatusCauseInfo(Enum):
        CAUSE_UNSPECIFIED = 0
        CAUSE_CANCELLED_BY_CLIENT = 15
        CAUSE_CANCELLED_BY_EXCHANGE = 1
        CAUSE_CANCELLED_NOT_ENOUGH_POSITION = 2
        CAUSE_CANCELLED_BY_CLIENT_BLOCK = 3
        CAUSE_REJECTED_BY_BROKER = 4
        CAUSE_REJECTED_BY_EXCHANGE = 5
        CAUSE_CANCELLED_BY_BROKER = 6


class OrderDirection(Enum):
    ORDER_DIRECTION_UNSPECIFIED = 0
    ORDER_DIRECTION_BUY = 1
    ORDER_DIRECTION_SELL = 2


class OrderType(Enum):
    ORDER_TYPE_UNSPECIFIED = 0
    ORDER_TYPE_LIMIT = 1
    ORDER_TYPE_MARKET = 2
    ORDER_TYPE_BESTPRICE = 3


class OrderExecutionReportStatus(Enum):
    EXECUTION_REPORT_STATUS_UNSPECIFIED = 0
    EXECUTION_REPORT_STATUS_FILL = 1
    EXECUTION_REPORT_STATUS_REJECTED = 2
    EXECUTION_REPORT_STATUS_CANCELLED = 3
    EXECUTION_REPORT_STATUS_NEW = 4
    EXECUTION_REPORT_STATUS_PARTIALLYFILL = 5


class TimeInForceType(Enum):
    TIME_IN_FORCE_UNSPECIFIED = 0
    TIME_IN_FORCE_DAY = 1
    TIME_IN_FORCE_FILL_AND_KILL = 2
    TIME_IN_FORCE_FILL_OR_KILL = 3
