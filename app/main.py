from fastapi import FastAPI
from app.api.routes.price import router as prices_router


app = FastAPI(
    title="Crypto Price API",
    description="API for stored BTC_USD and ETH_USD prices from Deribit",
)


@app.get("/")
def home_page():
    return {"message": "Привет!"}


app.include_router(prices_router)
