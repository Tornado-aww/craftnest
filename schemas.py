from typing import List, Literal
from pydantic import BaseModel, EmailStr, Field

class CartItem(BaseModel):
    product_id: int
    qty: int
    unit_price: float  # USD

class CheckoutRequest(BaseModel):
    customer_name: str = Field(min_length=2)
    email: EmailStr
    phone: str = Field(min_length=5)
    currency: Literal["USD"] = "USD"
    items: List[CartItem]
    comment: str | None = None
