from typing import Optional, Sequence
from datetime import date
from pydantic import BaseModel, EmailStr, conint



class UserBase(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr] = None
    birthday: Optional[date] = None
    privilege: conint(ge=1, le=3)# 1: ADMIN, 2: VENDEDOR, 3: CLIENTE

# Properties to recieve via API on creation
class UserCreate(UserBase):
    first_name: str
    email: EmailStr
    birthday: date
    password: str
    privilege: conint(ge=1, le=3)


# Properties to recieve via API on update
class UserUpdate(UserBase):
    ...


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional preoperties stored in DB but not returned by APi
class UserInDB(UserInDBBase):
    hashed_password: Optional[str] = None


# Additional properties to return via API
class User(UserInDBBase):
    ...


# Admin can search users
class UserSearchResults(UserInDBBase):
    results: Sequence[User]
