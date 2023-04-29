from typing import Optional, List

from pydantic import BaseModel, EmailStr



class ProductoBase(BaseModel):
    name: Optional[str]
    quantity: Optional[int]
    price: Optional[int]


# Properties to recieve via API on creation
class ProductoCreate(ProductoBase):
    name: Optional[str]
    quantity: Optional[int]
    description: Optional[str]
    price: Optional[int]


# Properties to recieve via API on update
class ProductoUpdate(ProductoBase):
    name: Optional[str]
    quantity: Optional[int]
    description: Optional[str]
    price: Optional[int]


class ProductoInDBBase(ProductoBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True

# Additional properties to return via API
class Producto(ProductoInDBBase):
    ...


# Additional preoperties stored in DB but not returned by APi
class ProductoInDB(ProductoInDBBase):
    ...

class ProductoSearchResults(ProductoInDBBase):
    results: List[Producto]
