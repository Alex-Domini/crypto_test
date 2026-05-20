import asyncio
import httpx

from app.celery_app import celery_app
from app.core.db import AsyncSessionLocal

from app.repositories.price_repository import PriceRepository
from app.services.deribit_client import DeribitClient
from app.services.price_service import PriceService


async def _run_fetch_and_save_prices() -> None:
    async with AsyncSessionLocal() as session:
        async with httpx.AsyncClient() as client:
            repository = PriceRepository(session)
            deribit_client = DeribitClient(client)
            service = PriceService(repository, deribit_client)

            saved_prices = await service.fetch_and_save_prices()

            for price in saved_prices:
                print(f"Saved: {price.ticker} {price.price} {price.timestamp}")


@celery_app.task(name="app.tasks.price_tasks.fetch_and_save_prices_task")
def fetch_and_save_prices_task() -> None:
    asyncio.run(_run_fetch_and_save_prices())
