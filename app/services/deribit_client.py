import httpx
from decimal import Decimal


class DeribitClient:
    BASE_URL = "https://www.deribit.com/api/v2/public/get_index_price"

    def __init__(self, client: httpx.AsyncClient) -> None:
        self.client = client

    async def get_index_price(self, index_name: str) -> Decimal:
        params = {"index_name": index_name.lower()}
        response = await self.client.get(
            self.BASE_URL,
            params=params,
        )
        response.raise_for_status()
        data = response.json()

        result = data.get("result")
        if result is None:
            raise ValueError("Deribit response does not contain 'result'")

        index_price = result.get("index_price")
        if index_price is None:
            raise ValueError("Deribit response does not contain 'index_price'")

        return Decimal(str(index_price))
