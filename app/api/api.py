from fastapi import APIRouter
from app.api.endpoints import currency_pair, exchange_rate

api_router = APIRouter()
api_router.include_router(currency_pair.router)
api_router.include_router(exchange_rate.router)
