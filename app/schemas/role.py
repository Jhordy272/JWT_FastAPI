from pydantic import BaseModel
from typing import Optional

class RoleBase(BaseModel):
    name: str

class RoleCreate(RoleBase):
    pass

class RoleResponse(RoleBase):
    id: int

    class Config:
        orm_mode = True

class RoleUpdate(BaseModel):
    name: str

    class Config:
        orm_mode = True