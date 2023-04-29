from typing import List, Literal, Optional, Sequence

from pydantic import BaseModel, EmailStr

from app.schemas.order_item import OrderItem, OrderItemCreate



class OrderBase(BaseModel):
    status: Optional[Literal["pending", "completed", "cancelled"]] = None
    owner_id: Optional[int] = None

# Properties to recieve via API on creation
class OrderCreate(OrderBase):
    status: Literal["pending", "completed", "cancelled"]
    owner_id: int
    order_items: List[OrderItemCreate] = []

# Properties to recieve via API on update
class OrderUpdate(OrderBase):
    id: int


class OrderInDBBase(OrderBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True

# Additional properties to return via API
class Order(OrderInDBBase):
    order_items: List[OrderItem] = []
    ...


# Additional preoperties stored in DB but not returned by APi
class OrderInDB(OrderInDBBase):
    ...

class OrderSearchResults(BaseModel):
    results: Sequence[Order]
