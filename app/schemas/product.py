from typing import Optional, List

from pydantic import BaseModel, EmailStr



class ProductBase(BaseModel):
    id: Optional[int] = None
    name: Optional[str]
    quantity: Optional[int]
    price: Optional[int]


# Properties to recieve via API on creation
class ProductCreate(ProductBase):
    name: Optional[str]
    quantity: Optional[int]
    description: Optional[str]
    price: Optional[int]


# Properties to recieve via API on update
class ProductUpdate(ProductBase):
    name: Optional[str]
    quantity: Optional[int]
    description: Optional[str]
    price: Optional[int]


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

class ProductSearchResults(ProductInDBBase):
    results: List[Product]
