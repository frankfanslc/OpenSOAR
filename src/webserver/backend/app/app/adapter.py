from typing import Type, Optional
from pydantic import UUID4
from sqlalchemy.orm import Session
from . import models

from fastapi_users.db.base import BaseUserDatabase
from fastapi_users.models import UD


class NotSetOAuthAccountTableError(Exception):
    """
    OAuth table was not set in DB adapter but was needed.
    Raised when trying to create/update a user with OAuth accounts set
    but no table were specified in the DB adapter.
    """
    pass


class SQLAlchemyORMUserDatabase(BaseUserDatabase[UD]):
    database: Session

    def __init__(
            self,
            user_db_schema: Type[UD],
            database: Session,
            oauth_accounts=None
    ):
        super().__init__(user_db_schema)
        self.database = database
        self.oauth_accounts = oauth_accounts

    async def get(self, user_id: UUID4) -> Optional[UD]:
        return self.database.query(models.User).filter(models.User.id == user_id).first()

    async def get_by_email(self, email: str) -> Optional[UD]:
        return self.database.query(models.User).filter(models.User.email == email).first()

    async def get_by_oauth_account(self, oauth: str, account_id: str) -> Optional[UD]:
        if self.oauth_accounts is not None:
            return
        raise NotSetOAuthAccountTableError()

    async def create(self, user: UD) -> UD:
        user_dict = user.dict()
        db_user = models.User(**user_dict)

        number_of_users = self.database.query(models.User).count()
        if number_of_users == 0:
            db_user.is_superuser = True
            user.is_superuser = True

        self.database.add(db_user)
        self.database.commit()
        self.database.refresh(db_user)
        return user

    async def update(self, user: UD) -> UD:
        user_dict = user.dict()
        db_user = models.User(**user_dict)
        self.database.merge(db_user)
        self.database.commit()
        self.database.refresh(db_user)
        return user

    async def delete(self, user: UD) -> None:
        user_dict = user.dict()
        db_user = models.User(**user_dict)
        self.database.delete(db_user)
        self.database.commit()
        self.database.refresh(db_user)
