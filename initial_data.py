import logging
import csv
import asyncio
from datetime import date
from decimal import Decimal

from app.models import CurrencyPair

from app.db.session import SessionLocal

from sqlalchemy import text

from app.models.exchange_rate import ExchangeRate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


TABLES_TO_CLEAR = [ExchangeRate.__tablename__, CurrencyPair.__tablename__]


async def init() -> None:
    async with SessionLocal() as session:
        with open("app/init_data/exchange.csv", newline="") as csvfile:
            file_reader = csv.DictReader(csvfile)
            currency_pairs = []
            for currency in file_reader.fieldnames:
                currency_pair: list = currency.split("/")
                if len(currency_pair) == 2:
                    currency_pairs.append(
                        CurrencyPair(currency_code_one=currency_pair[0], currency_code_two=currency_pair[1])
                    )

            for table in TABLES_TO_CLEAR:
                await session.execute(text(f"TRUNCATE {table} CASCADE"))
            await session.commit()

            session.add_all(currency_pairs)
            await session.commit()

            currency_pairs_map = {f"{i.currency_code_one}/{i.currency_code_two}": i.id for i in currency_pairs}

            for row in file_reader:
                rate_date = date.fromisoformat(row["Date"])
                for pair, rate in row.items():
                    if pair == "Date":
                        continue

                    er = ExchangeRate(
                        currency_pair_id=currency_pairs_map[pair],
                        rate_date=rate_date,
                        rate=Decimal(rate),
                    )
                    session.add(er)

            await session.commit()


def main() -> None:
    logger.info("Importing initial data")
    asyncio.run(init())
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
