import datetime
from common import MoneyValue
from common import Quotation
from dataclasses import dataclass
from enum import Enum
from typing import List


@dataclass
class GetAccountsRequest:
    pass


@dataclass
class GetAccountsResponse:
    accounts: List['Account']


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
    unary_limits: List['UnaryLimit']
    stream_limits: List['StreamLimit']


@dataclass
class UnaryLimit:
    limit_per_minute: int
    methods: List[str]


@dataclass
class StreamLimit:
    limit: int
    streams: List[str]
    open: int


@dataclass
class GetInfoRequest:
    pass


@dataclass
class GetInfoResponse:
    prem_status: bool
    qual_status: bool
    qualified_for_work_with: List[str]
    tariff: str


class AccessLevel(Enum):
    ACCOUNT_ACCESS_LEVEL_UNSPECIFIED = 0
    ACCOUNT_ACCESS_LEVEL_FULL_ACCESS = 1
    ACCOUNT_ACCESS_LEVEL_READ_ONLY = 2
    ACCOUNT_ACCESS_LEVEL_NO_ACCESS = 3
