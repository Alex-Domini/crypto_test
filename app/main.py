from fastapi import FastAPI
from app.api.routes.price import router as all_prices
from app.api.routes.price import router as latest_price
from app.api.routes.price import router as price_by_date_range

from app.tasks.price_tasks import fetch_and_save_prices


app = FastAPI()


@app.get("/")
def home_page():
    return {"message": "Привет!"}


app.include_router(all_prices)
app.include_router(latest_price)
app.include_router(price_by_date_range)

fetch_and_save_prices.delay()
