from datetime import datetime
from typing import TypedDict


class BalanceInfo(TypedDict):
    balance: float
    currency: str


class CheckInfo(TypedDict):
    status: str
    user_id: int
    balance: float
    currency: str
    date_mod: datetime
    proxy_id: int
    proxy_status: bool
    proxy_time: float


class DeleteInfo(TypedDict):
    status: str
    user_id: int
    balance: float
    currency: str
    count: int
