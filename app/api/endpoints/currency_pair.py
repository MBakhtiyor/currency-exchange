from app.db.session import database
from fastapi_crudrouter import DatabasesCRUDRouter
from app.schemas.currency_pair import CurrencyPairSchema, CurrencyPairCreateSchema
from app import models
from app.db.base import Base

router = DatabasesCRUDRouter(
    schema=CurrencyPairSchema,
    create_schema=CurrencyPairCreateSchema,
    table=Base.metadata.tables[models.CurrencyPair.__tablename__],
    database=database,
)
