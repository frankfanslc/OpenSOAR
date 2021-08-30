from typing import List, Optional

from pydantic import BaseModel, UUID4
from fastapi_users import models


class IncidentBase(BaseModel):
    title: str
    status: Optional[str] = None
    description: Optional[str] = None


class IncidentCreate(IncidentBase):
    owner_id: UUID4


class Incident(IncidentBase):
    id: int
    owner_id: UUID4

    class Config:
        orm_mode = True


class User(models.BaseUser):
    # BASEUSER
    # id: Optional[UUID4] = None
    # email: Optional[EmailStr] = None
    # is_active: Optional[bool] = True
    # is_superuser: Optional[bool] = False
    # is_verified: Optional[bool] = False
    incidents: List[Incident] = []
    display_name: Optional[str]

    class Config:
        orm_mode = True


class IncidentRead(Incident):
    owner: User


class UserCreate(models.BaseUserCreate):
    # BASEUSERCREATE
    # email: EmailStr
    # password: str
    # is_active: Optional[bool] = True
    # is_superuser: Optional[bool] = False
    # is_verified: Optional[bool] = False
    display_name: Optional[str]


class UserUpdate(User, models.BaseUserUpdate):
    # BASEUSER
    # id: Optional[UUID4] = None
    # email: Optional[EmailStr] = None
    # is_active: Optional[bool] = True
    # is_superuser: Optional[bool] = False
    # is_verified: Optional[bool] = False
    # BASEUSERUPDATE
    # password: Optional[str]
    pass


class UserDB(User, models.BaseUserDB):
    # BASEUSERDB
    # id: UUID4
    # email: EmailStr
    # is_active: bool
    # is_superuser: bool
    # is_verified: bool
    # hashed_password: str
    pass
