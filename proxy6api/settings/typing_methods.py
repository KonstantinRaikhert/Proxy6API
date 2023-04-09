from datetime import datetime
from typing import NamedTuple


class ErrorInfo(NamedTuple):
    error_id: int
    error: str


class BalanceInfo(NamedTuple):
    balance: float
    currency: str


class CheckInfo(NamedTuple):
    status: str
    user_id: int
    balance: float
    currency: str
    date_mod: datetime
    proxy_id: int
    proxy_status: bool
    proxy_time: float


class DeleteInfo(NamedTuple):
    status: str
    user_id: int
    balance: float
    currency: str
    count: int


class PriceInfo(NamedTuple):
    status: str
    user_id: int
    balance: float
    currency: str
    price: float
    price_single: float
    period: int
    count: int


class CountInfo(NamedTuple):
    status: str
    user_id: int
    balance: float
    currency: str
    count: int


class CountriesInfo(NamedTuple):
    status: str
    user_id: int
    balance: float
    currency: str
    countries_list: list[str]


class ProxyItemInfo(NamedTuple):
    id: int
    ip: str
    host: str
    port: str
    user: str
    password: str
    proxy_type: str
    country: str
    date: datetime
    date_end: datetime
    unixtime: int
    unixtime_end: int
    descr: str
    active: bool


class ProxyInfo(NamedTuple):
    status: str
    user_id: int
    balance: float
    currency: str
    list_count: int
    date_mod: datetime
    proxies_list: list[ProxyItemInfo]
    page: int


class SetTypeInfo(NamedTuple):
    status: str
    user_id: int
    balance: float
    currency: str


class SetDescrInfo(NamedTuple):
    status: str
    user_id: int
    balance: float
    currency: str
    count: int


class BuyInfo(NamedTuple):
    status: str
    user_id: int
    balance: float
    currency: str
    count: int
    date_mod: datetime
    price: float
    period: int
    country: str
    proxies_list: list[ProxyItemInfo]


class ProlongItemInfo(NamedTuple):
    id: int
    date_end: datetime
    unixtime_end: int


class ProlongInfo(NamedTuple):
    pass
