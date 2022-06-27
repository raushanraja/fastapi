from datetime import datetime
from pydantic import BaseModel, UUID4
from typing import Optional


class AddressBase(BaseModel):
    address: Optional[str] = None
    created_at: Optional[datetime] = None

class AddressCreate(AddressBase):
    address: str
    created_at: Optional[datetime] = datetime.utcnow()

class AddressUpdate(AddressBase):
    id: UUID4

class AddressInDBBase(AddressBase):
    id: UUID4

    class Config:
        orm_mode = True

class Address(AddressInDBBase):
    pass

class AddressInDB(AddressInDBBase):
    pass

