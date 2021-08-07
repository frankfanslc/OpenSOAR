from typing import Optional

from pydantic import BaseModel
from fastapi_users import models
from fastapi_users.db import SQLAlchemyUserDatabase
from .models import User as UserTable
from .database import database


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


# class UserBase(BaseModel):
#     email: str
#
#
# class UserCreate(UserBase):
#     password: str
#
#
# class User(UserBase):
#     id: int
#     is_active: bool
#     incidents: List[Incident] = []
#
#     class Config:
#         orm_mode = True

class User(models.BaseUser):
    pass


class UserCreate(models.BaseUserCreate):
    pass


class UserUpdate(User, models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    pass


users = UserTable.__table__
user_db = SQLAlchemyUserDatabase(UserDB, database, users)
