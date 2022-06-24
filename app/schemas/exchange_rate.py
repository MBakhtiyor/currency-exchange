from pydantic import BaseModel
from datetime import date
from decimal import Decimal


class ExchangeRateCreateSchema(BaseModel):
    currency_pair_id: int
    rate_date: date
    rate: Decimal


class ExchangeRateSchema(ExchangeRateCreateSchema):
    id: int

    class Config:
        orm_mode = True


class HistoryRateSchema(BaseModel):
    rate_date: date
    rate: Decimal

    class Config:
        orm_mode = True


class RateWithPathSchema(HistoryRateSchema):
    path: list[str]
