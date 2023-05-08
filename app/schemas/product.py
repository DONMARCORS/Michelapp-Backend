from typing import Optional, Sequence

from pydantic import BaseModel

class ProductBase(BaseModel):
    name: Optional[str]
    quantity: Optional[int]
    description: Optional[str]
    price: Optional[int]


# Properties to recieve via API on creation
class ProductCreate(ProductBase):
    id: int
    name: str
    quantity: int
    description: str
    price: int

# Properties to recieve via API on update
class ProductUpdate(ProductBase):
    ...

class ProductInDBBase(ProductBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True # This will allow us to use the class as a Pydantic model

# Additional properties to return via API
class Product(ProductInDBBase):
    ...

# Additional preoperties stored in DB but not returned by APi
class ProductInDB(ProductInDBBase):
    ...

class ProductSearchResults(BaseModel):
    results: Sequence[Product]
