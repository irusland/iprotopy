from common import MoneyValue
from common import MoneyValue
from operations import OperationState
from common import MoneyValue
from common import MoneyValue
from common import MoneyValue
from common import MoneyValue
from common import MoneyValue
from common import MoneyValue
from common import Quotation
from common import MoneyValue
from common import MoneyValue
from common import MoneyValue
from common import MoneyValue
from common import MoneyValue
from common import MoneyValue
from common import MoneyValue
from common import MoneyValue
from common import Quotation
from common import MoneyValue
from common import Quotation
from common import MoneyValue
from common import Quotation
from common import MoneyValue
from common import MoneyValue
from common import Quotation
from common import Quotation
from common import MoneyValue
from common import Quotation
from common import Quotation
from common import MoneyValue
from common import Quotation
from common import Quotation
from common import MoneyValue
from common import MoneyValue
from common import MoneyValue
from common import MoneyValue
from common import Quotation
from common import MoneyValue
from common import MoneyValue
from common import MoneyValue
from common import MoneyValue
from common import Quotation
from common import Quotation
from common import Quotation
from common import Quotation
from common import Quotation
from common import Quotation
from operations import OperationType
from operations import OperationState
from operations import OperationType
from operations import OperationState
from common import InstrumentType
from common import MoneyValue
from common import MoneyValue
from common import MoneyValue
from common import MoneyValue
from common import Quotation
from common import MoneyValue
from common import MoneyValue
from common import MoneyValue
from common import Quotation
from operations import PositionsSecurities
from operations import PositionsFutures
from operations import PositionsOptions
from common import MoneyValue
from common import MoneyValue
import datetime
from enum import Enum
from dataclasses import dataclass
from typing import List


@dataclass
class OperationsRequest:
    account_id: str
    from_: datetime
    to: datetime
    state: 'OperationState'
    figi: str


@dataclass
class OperationsResponse:
    operations: List['Operation']


@dataclass
class Operation:
    id: str
    parent_operation_id: str
    currency: str
    payment: 'MoneyValue'
    price: 'MoneyValue'
    state: 'OperationState'
    quantity: int
    quantity_rest: int
    figi: str
    instrument_type: str
    date: datetime
    type: str
    operation_type: 'OperationType'
    trades: List['OperationTrade']
    asset_uid: str
    position_uid: str
    instrument_uid: str


@dataclass
class OperationTrade:
    trade_id: str
    date_time: datetime
    quantity: int
    price: 'MoneyValue'


@dataclass
class PortfolioRequest:
    account_id: str
    currency: 'CurrencyRequest'


    class CurrencyRequest(Enum):
        RUB = 0
        USD = 1
        EUR = 2


@dataclass
class PortfolioResponse:
    total_amount_shares: 'MoneyValue'
    total_amount_bonds: 'MoneyValue'
    total_amount_etf: 'MoneyValue'
    total_amount_currencies: 'MoneyValue'
    total_amount_futures: 'MoneyValue'
    expected_yield: 'Quotation'
    positions: List['PortfolioPosition']
    account_id: str
    total_amount_options: 'MoneyValue'
    total_amount_sp: 'MoneyValue'
    total_amount_portfolio: 'MoneyValue'
    virtual_positions: List['VirtualPortfolioPosition']


@dataclass
class PositionsRequest:
    account_id: str


@dataclass
class PositionsResponse:
    money: List['MoneyValue']
    blocked: List['MoneyValue']
    securities: List['PositionsSecurities']
    limits_loading_in_progress: bool
    futures: List['PositionsFutures']
    options: List['PositionsOptions']


@dataclass
class WithdrawLimitsRequest:
    account_id: str


@dataclass
class WithdrawLimitsResponse:
    money: List['MoneyValue']
    blocked: List['MoneyValue']
    blocked_guarantee: List['MoneyValue']


@dataclass
class PortfolioPosition:
    figi: str
    instrument_type: str
    quantity: 'Quotation'
    average_position_price: 'MoneyValue'
    expected_yield: 'Quotation'
    current_nkd: 'MoneyValue'
    average_position_price_pt: 'Quotation'
    current_price: 'MoneyValue'
    average_position_price_fifo: 'MoneyValue'
    quantity_lots: 'Quotation'
    blocked: bool
    blocked_lots: 'Quotation'
    position_uid: str
    instrument_uid: str
    var_margin: 'MoneyValue'
    expected_yield_fifo: 'Quotation'


@dataclass
class VirtualPortfolioPosition:
    position_uid: str
    instrument_uid: str
    figi: str
    instrument_type: str
    quantity: 'Quotation'
    average_position_price: 'MoneyValue'
    expected_yield: 'Quotation'
    expected_yield_fifo: 'Quotation'
    expire_date: datetime
    current_price: 'MoneyValue'
    average_position_price_fifo: 'MoneyValue'


@dataclass
class PositionsSecurities:
    figi: str
    blocked: int
    balance: int
    position_uid: str
    instrument_uid: str
    exchange_blocked: bool
    instrument_type: str


@dataclass
class PositionsFutures:
    figi: str
    blocked: int
    balance: int
    position_uid: str
    instrument_uid: str


@dataclass
class PositionsOptions:
    position_uid: str
    instrument_uid: str
    blocked: int
    balance: int


@dataclass
class BrokerReportRequest:
    pass


@dataclass
class BrokerReportResponse:
    pass


@dataclass
class GenerateBrokerReportRequest:
    account_id: str
    from_: datetime
    to: datetime


@dataclass
class GenerateBrokerReportResponse:
    task_id: str


@dataclass
class GetBrokerReportRequest:
    task_id: str
    page: int


@dataclass
class GetBrokerReportResponse:
    broker_report: List['BrokerReport']
    itemsCount: int
    pagesCount: int
    page: int


@dataclass
class BrokerReport:
    trade_id: str
    order_id: str
    figi: str
    execute_sign: str
    trade_datetime: datetime
    exchange: str
    class_code: str
    direction: str
    name: str
    ticker: str
    price: 'MoneyValue'
    quantity: int
    order_amount: 'MoneyValue'
    aci_value: 'Quotation'
    total_order_amount: 'MoneyValue'
    broker_commission: 'MoneyValue'
    exchange_commission: 'MoneyValue'
    exchange_clearing_commission: 'MoneyValue'
    repo_rate: 'Quotation'
    party: str
    clear_value_date: datetime
    sec_value_date: datetime
    broker_status: str
    separate_agreement_type: str
    separate_agreement_number: str
    separate_agreement_date: str
    delivery_type: str


class OperationState(Enum):
    OPERATION_STATE_UNSPECIFIED = 0
    OPERATION_STATE_EXECUTED = 1
    OPERATION_STATE_CANCELED = 2
    OPERATION_STATE_PROGRESS = 3


class OperationType(Enum):
    OPERATION_TYPE_UNSPECIFIED = 0
    OPERATION_TYPE_INPUT = 1
    OPERATION_TYPE_BOND_TAX = 2
    OPERATION_TYPE_OUTPUT_SECURITIES = 3
    OPERATION_TYPE_OVERNIGHT = 4
    OPERATION_TYPE_TAX = 5
    OPERATION_TYPE_BOND_REPAYMENT_FULL = 6
    OPERATION_TYPE_SELL_CARD = 7
    OPERATION_TYPE_DIVIDEND_TAX = 8
    OPERATION_TYPE_OUTPUT = 9
    OPERATION_TYPE_BOND_REPAYMENT = 10
    OPERATION_TYPE_TAX_CORRECTION = 11
    OPERATION_TYPE_SERVICE_FEE = 12
    OPERATION_TYPE_BENEFIT_TAX = 13
    OPERATION_TYPE_MARGIN_FEE = 14
    OPERATION_TYPE_BUY = 15
    OPERATION_TYPE_BUY_CARD = 16
    OPERATION_TYPE_INPUT_SECURITIES = 17
    OPERATION_TYPE_SELL_MARGIN = 18
    OPERATION_TYPE_BROKER_FEE = 19
    OPERATION_TYPE_BUY_MARGIN = 20
    OPERATION_TYPE_DIVIDEND = 21
    OPERATION_TYPE_SELL = 22
    OPERATION_TYPE_COUPON = 23
    OPERATION_TYPE_SUCCESS_FEE = 24
    OPERATION_TYPE_DIVIDEND_TRANSFER = 25
    OPERATION_TYPE_ACCRUING_VARMARGIN = 26
    OPERATION_TYPE_WRITING_OFF_VARMARGIN = 27
    OPERATION_TYPE_DELIVERY_BUY = 28
    OPERATION_TYPE_DELIVERY_SELL = 29
    OPERATION_TYPE_TRACK_MFEE = 30
    OPERATION_TYPE_TRACK_PFEE = 31
    OPERATION_TYPE_TAX_PROGRESSIVE = 32
    OPERATION_TYPE_BOND_TAX_PROGRESSIVE = 33
    OPERATION_TYPE_DIVIDEND_TAX_PROGRESSIVE = 34
    OPERATION_TYPE_BENEFIT_TAX_PROGRESSIVE = 35
    OPERATION_TYPE_TAX_CORRECTION_PROGRESSIVE = 36
    OPERATION_TYPE_TAX_REPO_PROGRESSIVE = 37
    OPERATION_TYPE_TAX_REPO = 38
    OPERATION_TYPE_TAX_REPO_HOLD = 39
    OPERATION_TYPE_TAX_REPO_REFUND = 40
    OPERATION_TYPE_TAX_REPO_HOLD_PROGRESSIVE = 41
    OPERATION_TYPE_TAX_REPO_REFUND_PROGRESSIVE = 42
    OPERATION_TYPE_DIV_EXT = 43
    OPERATION_TYPE_TAX_CORRECTION_COUPON = 44
    OPERATION_TYPE_CASH_FEE = 45
    OPERATION_TYPE_OUT_FEE = 46
    OPERATION_TYPE_OUT_STAMP_DUTY = 47
    OPERATION_TYPE_OUTPUT_SWIFT = 50
    OPERATION_TYPE_INPUT_SWIFT = 51
    OPERATION_TYPE_OUTPUT_ACQUIRING = 53
    OPERATION_TYPE_INPUT_ACQUIRING = 54
    OPERATION_TYPE_OUTPUT_PENALTY = 55
    OPERATION_TYPE_ADVICE_FEE = 56
    OPERATION_TYPE_TRANS_IIS_BS = 57
    OPERATION_TYPE_TRANS_BS_BS = 58
    OPERATION_TYPE_OUT_MULTI = 59
    OPERATION_TYPE_INP_MULTI = 60
    OPERATION_TYPE_OVER_PLACEMENT = 61
    OPERATION_TYPE_OVER_COM = 62
    OPERATION_TYPE_OVER_INCOME = 63
    OPERATION_TYPE_OPTION_EXPIRATION = 64
    OPERATION_TYPE_FUTURE_EXPIRATION = 65


@dataclass
class GetDividendsForeignIssuerRequest:
    pass


@dataclass
class GetDividendsForeignIssuerResponse:
    pass


@dataclass
class GenerateDividendsForeignIssuerReportRequest:
    account_id: str
    from_: datetime
    to: datetime


@dataclass
class GetDividendsForeignIssuerReportRequest:
    task_id: str
    page: int


@dataclass
class GenerateDividendsForeignIssuerReportResponse:
    task_id: str


@dataclass
class GetDividendsForeignIssuerReportResponse:
    dividends_foreign_issuer_report: List['DividendsForeignIssuerReport']
    itemsCount: int
    pagesCount: int
    page: int


@dataclass
class DividendsForeignIssuerReport:
    record_date: datetime
    payment_date: datetime
    security_name: str
    isin: str
    issuer_country: str
    quantity: int
    dividend: 'Quotation'
    external_commission: 'Quotation'
    dividend_gross: 'Quotation'
    tax: 'Quotation'
    dividend_amount: 'Quotation'
    currency: str


@dataclass
class PortfolioStreamRequest:
    accounts: List[str]


@dataclass
class PortfolioStreamResponse:
    pass


@dataclass
class PortfolioSubscriptionResult:
    accounts: List['AccountSubscriptionStatus']


@dataclass
class AccountSubscriptionStatus:
    account_id: str
    subscription_status: 'PortfolioSubscriptionStatus'


class PortfolioSubscriptionStatus(Enum):
    PORTFOLIO_SUBSCRIPTION_STATUS_UNSPECIFIED = 0
    PORTFOLIO_SUBSCRIPTION_STATUS_SUCCESS = 1
    PORTFOLIO_SUBSCRIPTION_STATUS_ACCOUNT_NOT_FOUND = 2
    PORTFOLIO_SUBSCRIPTION_STATUS_INTERNAL_ERROR = 3


@dataclass
class GetOperationsByCursorRequest:
    account_id: str
    instrument_id: str
    from_: datetime
    to: datetime
    cursor: str
    limit: int
    operation_types: List['OperationType']
    state: 'OperationState'
    without_commissions: bool
    without_trades: bool
    without_overnights: bool


@dataclass
class GetOperationsByCursorResponse:
    has_next: bool
    next_cursor: str
    items: List['OperationItem']


@dataclass
class OperationItem:
    cursor: str
    broker_account_id: str
    id: str
    parent_operation_id: str
    name: str
    date: datetime
    type: 'OperationType'
    description: str
    state: 'OperationState'
    instrument_uid: str
    figi: str
    instrument_type: str
    instrument_kind: 'InstrumentType'
    position_uid: str
    payment: 'MoneyValue'
    price: 'MoneyValue'
    commission: 'MoneyValue'
    yield_: 'MoneyValue'
    yield_relative: 'Quotation'
    accrued_int: 'MoneyValue'
    quantity: int
    quantity_rest: int
    quantity_done: int
    cancel_date_time: datetime
    cancel_reason: str
    trades_info: 'OperationItemTrades'
    asset_uid: str


@dataclass
class OperationItemTrades:
    trades: List['OperationItemTrade']


@dataclass
class OperationItemTrade:
    num: str
    date: datetime
    quantity: int
    price: 'MoneyValue'
    yield_: 'MoneyValue'
    yield_relative: 'Quotation'


@dataclass
class PositionsStreamRequest:
    accounts: List[str]


@dataclass
class PositionsStreamResponse:
    pass


@dataclass
class PositionsSubscriptionResult:
    accounts: List['PositionsSubscriptionStatus']


@dataclass
class PositionsSubscriptionStatus:
    account_id: str
    subscription_status: 'PositionsAccountSubscriptionStatus'


class PositionsAccountSubscriptionStatus(Enum):
    POSITIONS_SUBSCRIPTION_STATUS_UNSPECIFIED = 0
    POSITIONS_SUBSCRIPTION_STATUS_SUCCESS = 1
    POSITIONS_SUBSCRIPTION_STATUS_ACCOUNT_NOT_FOUND = 2
    POSITIONS_SUBSCRIPTION_STATUS_INTERNAL_ERROR = 3


@dataclass
class PositionData:
    account_id: str
    money: List['PositionsMoney']
    securities: List['PositionsSecurities']
    futures: List['PositionsFutures']
    options: List['PositionsOptions']
    date: datetime


@dataclass
class PositionsMoney:
    available_value: 'MoneyValue'
    blocked_value: 'MoneyValue'
