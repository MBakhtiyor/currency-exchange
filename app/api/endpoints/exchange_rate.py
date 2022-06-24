from typing import Union

from app.db.session import database
from fastapi import Query, HTTPException, APIRouter
from app.schemas.exchange_rate import (
    HistoryRateSchema,
    RateWithPathSchema,
)
from app import models
from sqlalchemy import select

from decimal import Decimal, getcontext
import datetime
from itertools import permutations


getcontext().prec = 4
DATE_REGEXP = r"^\d{4}-\d{2}-\d{2}$"

router = APIRouter()


@router.get("/history", response_model=list[HistoryRateSchema])
async def history(
    currency_pair: str = Query(default=..., min_length=7, max_length=7, regex="^[A-Z]{3}/[A-Z]{3}$", example="EUR/USD"),
    start_date: str = Query(default=..., min_length=10, max_length=10, regex=DATE_REGEXP, example="2020-01-17"),
    end_date: str = Query(default=..., min_length=10, max_length=10, regex=DATE_REGEXP, example="2020-01-31"),
):
    """Get history data for currency pair"""
    currency_code_one, currency_code_two = currency_pair.split("/")
    query = (
        select(models.ExchangeRate)
        .join(models.ExchangeRate.currency_pair)
        .where(
            models.CurrencyPair.currency_code_one == currency_code_one,
            models.CurrencyPair.currency_code_two == currency_code_two,
        )
    )
    if start_date:
        query = query.where(models.ExchangeRate.rate_date >= datetime.date.fromisoformat(start_date))

    if end_date:
        query = query.where(models.ExchangeRate.rate_date <= datetime.date.fromisoformat(end_date))

    rates = await database.fetch_all(query)

    return [HistoryRateSchema.from_orm(i) for i in rates]


@router.get("/rate", response_model=Union[RateWithPathSchema, HistoryRateSchema])
async def rate(
    currency_pair: str = Query(default=..., min_length=7, max_length=7, regex="^[A-Z]{3}/[A-Z]{3}$", example="EUR/USD"),
    date: str = Query(default=..., min_length=10, max_length=10, regex=DATE_REGEXP, example="2020-01-17"),
):
    """Get rate for rate_date and currency pair"""
    currency_code_one, currency_code_two = currency_pair.split("/")
    if currency_code_one == currency_code_two:
        return HistoryRateSchema(rate_date=datetime.date.fromisoformat(date), rate=Decimal("1.0000"))

    query = select(models.ExchangeRate).where(models.ExchangeRate.rate_date == datetime.date.fromisoformat(date))
    rates = await database.fetch_all(query)

    currencies = set()
    currency_pair_rate = {}

    for i in rates:
        currencies.add(i.currency_code_one)
        currencies.add(i.currency_code_two)
        currency_pair_rate[(i.currency_code_one, i.currency_code_two)] = i.rate
        currency_pair_rate[(i.currency_code_two, i.currency_code_one)] = Decimal(1) / i.rate

    if (currency_code_one, currency_code_two) in currency_pair_rate:
        return RateWithPathSchema(
            rate_date=datetime.date.fromisoformat(date),
            rate=currency_pair_rate[(currency_code_one, currency_code_two)],
            path=[currency_code_one, currency_code_two],
        )

    min_rate = Decimal("Inf")
    min_path = None

    currencies.difference_update({currency_code_one, currency_code_two})
    currencies = list(currencies)
    for i in range(len(currencies) + 1):
        for path in permutations(currencies, i):
            path = list(path)
            path.insert(0, currency_code_one)
            path.append(currency_code_two)
            rate = Decimal(1)

            for code_one, code_two in zip(path, path[1:]):
                if (code_one, code_two) not in currency_pair_rate:
                    break
                rate *= currency_pair_rate[(code_one, code_two)]
            else:
                if rate < min_rate:
                    min_rate = rate
                    min_path = path

    if not min_path:
        raise HTTPException(status_code=400, detail="Conversion not found")
    else:
        return RateWithPathSchema(rate_date=datetime.date.fromisoformat(date), rate=min_rate, path=min_path)
