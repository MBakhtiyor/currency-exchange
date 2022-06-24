from pydantic import BaseModel


class CurrencyPairCreateSchema(BaseModel):
    currency_code_one: str
    currency_code_two: str


class CurrencyPairSchema(CurrencyPairCreateSchema):
    id: int

    class Config:
        orm_mode = True
