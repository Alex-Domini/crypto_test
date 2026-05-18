from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.price import PricePublic
from app.repositories.price_repository import PriceRepository
from app.core.db import get_db

router = APIRouter(prefix="/prices", tags=["Prices"])


@router.get("/history", response_model=list[PricePublic])
async def get_all_prices(
    ticker: str = Query(...), session: AsyncSession = Depends(get_db)
):
    repo = PriceRepository(session)
    prices = await repo.get_all_by_ticker(ticker.strip().upper())
    return prices


@router.get("/latest", response_model=PricePublic)
async def get_latest_price(
    ticker: str = Query(..., description="Тикер валюты"),
    session: AsyncSession = Depends(get_db),
):

    repo = PriceRepository(session)
    latest_price = await repo.get_latest_by_ticker(ticker.strip().upper())
    if latest_price is None:
        raise HTTPException(status_code=404, detail=f"Price for {ticker} not found")
    return latest_price


@router.get("/date_range", response_model=list[PricePublic])
async def get_price_by_date_range(
    ticker: str = Query(...),
    date_from: int = Query(...),
    date_to: int = Query(...),
    session: AsyncSession = Depends(get_db),
):

    repo = PriceRepository(session)
    date_range_prices = await repo.get_by_ticker_and_date_range(
        ticker.strip().upper(), date_from, date_to
    )

    return date_range_prices
