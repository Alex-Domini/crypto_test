from decimal import Decimal

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.price import Price


class PriceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, ticker: str, price: Decimal, timestamp: int) -> Price:
        price_obj = Price(
            ticker=ticker,
            price=price,
            timestamp=timestamp,
        )
        self.session.add(price_obj)
        await self.session.commit()
        await self.session.refresh(price_obj)
        return price_obj

    async def get_all_by_ticker(self) -> list[Price]:
        result = await self.session.execute(
            select(Price).order_by(Price.timestamp.asc())
        )
        return list(result.scalars().all())

    async def get_latest_by_ticker(self, ticker: str) -> Price | None:
        result = await self.session.execute(
            select(Price)
            .where(Price.ticker == ticker)
            .order_by(desc(Price.timestamp))
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def get_by_ticker_and_date_range(
        self,
        ticker: str,
        date_from: int,
        date_to: int,
    ) -> list[Price]:
        result = await self.session.execute(
            select(Price)
            .where(
                Price.ticker == ticker,
                Price.timestamp >= date_from,
                Price.timestamp <= date_to,
            )
            .order_by(Price.timestamp.asc())
        )
        return list(result.scalars().all())
