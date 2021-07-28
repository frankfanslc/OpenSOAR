from typing import List, Optional

from pydantic import BaseModel
from fastapi_users import models


class IncidentBase(BaseModel):
    title: str
    description: Optional[str] = None


class IncidentCreate(IncidentBase):
    pass


class Incident(IncidentBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class User(models.BaseUser):
    incidents: List[Incident] = []
    id: int

    class Config:
        orm_mode = True


class UserCreate(models.BaseUserCreate):
    pass


class UserUpdate(models.BaseUserCreate):
    pass


class UserDB(models.BaseUserDB):
    pass