from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.routes.price import router as prices_router

from app.tasks.price_tasks import fetch_and_save_prices_task


@asynccontextmanager
async def lifespan(app: FastAPI):
    fetch_and_save_prices_task.delay()
    yield


app = FastAPI(
    title="Crypto Price API",
    description="API for stored BTC_USD and ETH_USD prices from Deribit",
)


@app.get("/")
def home_page():
    return {"message": "Привет!"}


app.include_router(prices_router)
