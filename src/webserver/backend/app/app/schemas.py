from typing import List, Optional

from pydantic import BaseModel


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


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    incidents: List[Incident] = []

    class Config:
        orm_mode = True
