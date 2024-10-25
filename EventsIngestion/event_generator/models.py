from pydantic import BaseModel, Field, validator
from typing import List, Any


class BaseEvent(BaseModel):
    event_id: str = Field(..., min_length=1)
    event_category: str = Field(..., min_length=1)
    timestamp: int = Field(..., gt=0)
    user_id: str = Field(..., min_length=1)
    insert_id: str = Field(..., min_length=1)
    source_id: str = Field(..., min_length=1)
    device_id: str = Field(..., min_length=1)
    event_date: str = Field(..., min_length=1)

    @validator('*', pre=True)
    def trim_strings(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v


class SearchEvent(BaseEvent):
    search_query: str = Field(..., min_length=1)


class AddToCartEvent(BaseEvent):
    product_id: str = Field(..., min_length=1)
    product_name: str = Field(..., min_length=1)
    quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)


class PlaceOrderEvent(BaseEvent):
    order_id: str = Field(..., min_length=1)
    order_total: float = Field(..., gt=0)
    items: List[Any] = Field(..., min_items=1)


class ChargedEvent(BaseEvent):
    payment_method: str = Field(..., min_length=1)
    amount: float = Field(..., gt=0)


class LoginEvent(BaseEvent):
    login_method: str = Field(..., min_length=1)


class AppLaunchedEvent(BaseEvent):
    app_version: str = Field(..., min_length=1)
