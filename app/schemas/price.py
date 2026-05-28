from datetime import datetime, timezone
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field, computed_field


class PriceBase(BaseModel):
    ticker: str
    price: Decimal = Field(..., max_digits=18, decimal_places=2, examples=["0.00"])
    timestamp: int

    # человекочитаемое время, не храня его отдельно в БД
    @computed_field
    @property
    def datetime(self) -> str:
        return datetime.fromtimestamp(
            self.timestamp,
            tz=timezone.utc,
        ).isoformat()

    model_config = ConfigDict(from_attributes=True)


class PriceRead(PriceBase):
    id: int


class PricePublic(PriceBase):
    pass
