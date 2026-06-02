import time

from decimal import Decimal
from typing import Protocol

from app.models.price import Price
from app.repositories.price_repository import PriceRepository
from app.services.deribit_client import DeribitClient


class PriceRepositoryProtocol(Protocol):
    async def create(self, ticker: str, price: Decimal, timestamp: int) -> Price: ...


class DeribitClientProtocol(Protocol):
    async def get_index_price(self, index_name: str) -> Decimal: ...


class PriceService:
    INDEX_NAMES = ("BTC_USD", "ETH_USD")

    def __init__(
        self, repository: PriceRepositoryProtocol, client: DeribitClientProtocol
    ) -> None:
        self.repository = repository
        self.client = client

    async def fetch_and_save_prices(self) -> list[Price]:
        saved_prices: list[Price] = []
        current_timestamp = int(time.time())

        for index_name in self.INDEX_NAMES:
            price = await self.client.get_index_price(index_name)

            saved_price = await self.repository.create(
                ticker=index_name,
                price=price,
                timestamp=current_timestamp,
            )
            saved_prices.append(saved_price)
        return saved_prices
