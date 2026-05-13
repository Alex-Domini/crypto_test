from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.price import PriceRead
from app.repositories.price_repository import PriceRepository
from app.core.db import get_db

router = APIRouter(prefix="/prices", tags=["Prices"])


@router.get("/", response_model=list[PriceRead])
async def get_all_prices(session: AsyncSession = Depends(get_db)):
    repo = PriceRepository(session)
    prices = await repo.get_all_by_ticker()
    return prices


@router.get("/latest", response_model=PriceRead)
async def get_latest_price(
    ticker_name: str = Query(..., description="Тикер валюты"),
    session: AsyncSession = Depends(get_db),
):

    repo = PriceRepository(session)
    latest_price = await repo.get_latest_by_ticker(ticker_name.upper())
    if latest_price is None:
        raise HTTPException(
            status_code=404, detail=f"Price for {ticker_name} not found"
        )
    return latest_price


@router.get("/date_range", response_model=PriceRead)
async def get_price_by_date_range(
    ticker_name: str = Query(..., alias="ticker"),
    date_from: int = Query(...),
    date_to: int = Query(...),
    session: AsyncSession = Depends(get_db),
):

    repo = PriceRepository(session)
    date_range_price = await repo.get_by_ticker_and_date_range(
        ticker_name.upper(), date_from, date_to
    )

    if date_range_price is None:
        raise HTTPException(status_code=404, detail="Price not found")
    return date_range_price
