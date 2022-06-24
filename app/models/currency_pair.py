from sqlalchemy import Column, Integer, String, UniqueConstraint, CheckConstraint

from app.db.base_class import Base


class CurrencyPair(Base):
    __tablename__ = "currency_pairs"

    id = Column(Integer, primary_key=True, index=True)
    currency_code_one = Column(String(3), index=True, nullable=False)
    currency_code_two = Column(String(3), index=True, nullable=False)

    __table_args__ = (
        CheckConstraint("length(currency_code_one) == 3"),
        CheckConstraint("length(currency_code_two) == 3"),
        UniqueConstraint(currency_code_one, currency_code_two),
    )
