from decimal import Decimal
from app.models.price import Price

import pytest

from app.services.price_service import PriceService


class FakeDeribitClient:
    async def get_index_price(self, index_name: str) -> Decimal:
        prices = {
            "BTC_USD": Decimal("70000.00"),
            "ETH_USD": Decimal("3500.00"),
        }

        if index_name not in prices:
            raise ValueError(f"Unexpected index: {index_name}")
        return prices[index_name]


class FakePriceRepository:
    create_fake_repository = []

    async def create(self, ticker: str, price: Decimal, timestamp: int) -> Price:
        item = Price(
            id=1,  # Для тестов генерируем любой фейковый id
            ticker=ticker,
            price=price,
            timestamp=timestamp,
        )
        self.create_fake_repository.append(item)
        return item


@pytest.mark.asyncio
async def test_fetch_and_save_prices_returns_two_saved_prices():
    client = FakeDeribitClient()
    repository = FakePriceRepository()
    service = PriceService(repository=repository, client=client)

    result = await service.fetch_and_save_prices()

    assert len(result) == 2

    assert result[0].ticker == "BTC_USD"
    assert result[0].price == Decimal("70000.00")
    assert result[0].timestamp is not None

    assert result[1].ticker == "ETH_USD"
    assert result[1].price == Decimal("3500.00")

    assert len(repository.create_fake_repository) == 2
