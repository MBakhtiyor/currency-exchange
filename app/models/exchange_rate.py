from sqlalchemy import Column, Integer, Date, Numeric, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class ExchangeRate(Base):
    __tablename__ = "exchange_rates"

    id = Column(Integer, primary_key=True, index=True)
    currency_pair_id = Column(Integer, ForeignKey("currency_pairs.id"), nullable=False)
    currency_pair = relationship("CurrencyPair", lazy="joined")
    rate_date = Column(Date, index=True, nullable=False)
    rate = Column(Numeric(scale=4), nullable=False)

    __table_args__ = (UniqueConstraint(rate_date, currency_pair_id),)
