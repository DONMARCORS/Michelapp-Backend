from typing import Optional

from pydantic import BaseModel


class OrderItemBase(BaseModel):
    quantity: Optional[int]
    product_id: Optional[int]

# Properties to recieve via API on creation
class OrderItemCreate(OrderItemBase):
    quantity: int
    product_id: int


# Properties to recieve via API on update
class OrderItemUpdate(OrderItemBase):
    ...


class OrderItemInDBBase(OrderItemBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True

# Additional properties to return via API
class OrderItem(OrderItemInDBBase):
    ...


# Additional preoperties stored in DB but not returned by APi
class OrderItemInDB(OrderItemInDBBase):
    ...


