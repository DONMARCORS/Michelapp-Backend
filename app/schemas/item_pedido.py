from typing import Optional

from pydantic import BaseModel


class ItemPedidoBase(BaseModel):
    quantity: Optional[int]
    product_id: Optional[int]
    pedido_id: Optional[int]

# Properties to recieve via API on creation
class ItemPedidoCreate(ItemPedidoBase):
    quantity: int
    product_id: int
    pedido_id: int


# Properties to recieve via API on update
class ItemPedidoUpdate(ItemPedidoBase):
    ...


class ItemPedidoInDBBase(ItemPedidoBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True

# Additional properties to return via API
class ItemPedido(ItemPedidoInDBBase):
    ...


# Additional preoperties stored in DB but not returned by APi
class ItemPedidoInDB(ItemPedidoInDBBase):
    ...


