from pydantic import BaseModel, ConfigDict
from decimal import Decimal


class PriceRead(BaseModel):
    id: int
    ticker: str
    price: Decimal
    timestamp: int

    model_config = ConfigDict(from_attributes=True)


class PricePublic(BaseModel):
    ticker: str
    price: Decimal
    timestamp: int

    model_config = ConfigDict(from_attributes=True)
