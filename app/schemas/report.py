from typing import List, Literal, Optional, Sequence
from pydantic import BaseModel, EmailStr



class ReportBase(BaseModel):
    notas: str
    total: int
    owner_id: int
    rfc: str


# Properties to recieve via API on creation
class ReportCreate(ReportBase):
    notas: str
    total: int
    owner_id: int
    rfc: str

# Properties to recieve via API on update
class ReportUpdate(ReportBase):
    notas: str
    total: int
    rfc: str

class ReportInDBBase(ReportBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True

# Additional properties to return via API
class Report(ReportInDBBase):
    ...


# Additional preoperties stored in DB but not returned by APi
class ReportInDB(ReportInDBBase):
    ...

class ReportSearchResults(BaseModel):
    results: Sequence[Report]
