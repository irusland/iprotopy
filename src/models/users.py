from enum import Enum
from dataclasses import dataclass
import datetime


@dataclass
class GetAccountsRequest:
    pass


@dataclass
class GetAccountsResponse:
    accounts: 'Account'


@dataclass
class Account:
    id: str
    type: 'AccountType'
    name: str
    status: 'AccountStatus'
    opened_date: datetime
    closed_date: datetime
    access_level: 'AccessLevel'


class AccountType(Enum):
    ACCOUNT_TYPE_UNSPECIFIED = 0
    ACCOUNT_TYPE_TINKOFF = 1
    ACCOUNT_TYPE_TINKOFF_IIS = 2
    ACCOUNT_TYPE_INVEST_BOX = 3
    ACCOUNT_TYPE_INVEST_FUND = 4


class AccountStatus(Enum):
    ACCOUNT_STATUS_UNSPECIFIED = 0
    ACCOUNT_STATUS_NEW = 1
    ACCOUNT_STATUS_OPEN = 2
    ACCOUNT_STATUS_CLOSED = 3


@dataclass
class GetMarginAttributesRequest:
    account_id: str


@dataclass
class GetMarginAttributesResponse:
    liquid_portfolio: 'MoneyValue'
    starting_margin: 'MoneyValue'
    minimal_margin: 'MoneyValue'
    funds_sufficiency_level: 'Quotation'
    amount_of_missing_funds: 'MoneyValue'
    corrected_margin: 'MoneyValue'


@dataclass
class GetUserTariffRequest:
    pass


@dataclass
class GetUserTariffResponse:
    unary_limits: 'UnaryLimit'
    stream_limits: 'StreamLimit'


@dataclass
class UnaryLimit:
    limit_per_minute: int
    methods: str


@dataclass
class StreamLimit:
    limit: int
    streams: str
    open: int


@dataclass
class GetInfoRequest:
    pass


@dataclass
class GetInfoResponse:
    prem_status: 'bool'
    qual_status: 'bool'
    qualified_for_work_with: str
    tariff: str


class AccessLevel(Enum):
    ACCOUNT_ACCESS_LEVEL_UNSPECIFIED = 0
    ACCOUNT_ACCESS_LEVEL_FULL_ACCESS = 1
    ACCOUNT_ACCESS_LEVEL_READ_ONLY = 2
    ACCOUNT_ACCESS_LEVEL_NO_ACCESS = 3
