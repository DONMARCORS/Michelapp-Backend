from typing import Optional, Sequence

from pydantic import BaseModel, EmailStr



class PedidoBase(BaseModel):
    status: str
    owner_id: int


# Properties to recieve via API on creation
class PedidoCreate(PedidoBase):
    status: str
    owner_id: int


# Properties to recieve via API on update
class PedidoUpdate(PedidoBase):
    status : str


class PedidoInDBBase(PedidoBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True

# Additional properties to return via API
class Pedido(PedidoInDBBase):
    ...


# Additional preoperties stored in DB but not returned by APi
class PedidoInDB(PedidoInDBBase):
    ...

class PedidoSearchResults(BaseModel):
    results: Sequence[Pedido]
