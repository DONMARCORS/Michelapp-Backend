from typing import List, Literal, Optional, Sequence

from pydantic import BaseModel, EmailStr

from app.schemas.order_item import OrderItem, OrderItemCreate
from app.schemas.user import UserEmail, User



class OrderBase(BaseModel):
    status: Optional[Literal["realizado", "aceptado", "proceso", "enviado", "entregado", "cancelado"]] = None
    owner_id: Optional[int] = None
    created_at: Optional[str] = None


# Properties to recieve via API on creation
class OrderCreate(OrderBase):
    owner_id: int
    status: Literal["realizado", "aceptado", "proceso", "enviado", "entregado", "cancelado"]
    order_items: List[OrderItemCreate] = []

# Properties to recieve via API on update
class OrderUpdate(OrderBase):
    status: Literal["realizado", "aceptado", "proceso", "enviado", "entregado", "cancelado"]


class OrderInDBBase(OrderBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True

# Additional properties to return via API
class Order(OrderInDBBase):
    owner : User = None # We set this to User because we want to have a User object instead of an id
    order_items: List[OrderItem] = []
    ...


# Additional preoperties stored in DB but not returned by APi
class OrderInDB(OrderInDBBase):
    ...

class OrderSearchResults(BaseModel):
    results: Sequence[Order]
