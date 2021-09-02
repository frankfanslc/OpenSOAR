from typing import List, Dict, Union

from sse_starlette.sse import EventSourceResponse
from fastapi import Depends, FastAPI, Request
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import SessionLocal
from .adapter import SQLAlchemyORMUserDatabase
from .schemas import User, UserCreate, UserUpdate, UserDB
from .utils import incident_event_generator

db_session = SessionLocal()
user_db = SQLAlchemyORMUserDatabase(UserDB, db_session)
SECRET = "OpenSOAR@11042018"
auth_backends = []
jwt_authentication = JWTAuthentication(secret=SECRET, lifetime_seconds=3600, tokenUrl='auth/jwt/login')
auth_backends.append(jwt_authentication)

fastapi_users = FastAPIUsers(
    user_db,
    auth_backends,
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

app = FastAPI(root_path="/api")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {}


app.include_router(
    fastapi_users.get_auth_router(jwt_authentication),
    prefix="/auth/jwt",
    tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(),
    prefix="/users",
    tags=["users"],
)


@app.get("/users", response_model=List)
def read_users(db: Session = Depends(get_db),
               user: User = Depends(fastapi_users.current_user(active=True))
               ):
    return crud.read_users(db)


@app.get("/incidents", response_model=Dict[str, Union[List[schemas.IncidentRead], int]])
def read_incidents(skip: int = 0, limit: int = 10, query_filter: str = None,
                   db: Session = Depends(get_db),
                   user: User = Depends(fastapi_users.current_user(active=True))
                   ):
    return crud.get_incidents(db, skip=skip, limit=limit, query_filter=query_filter)


@app.post("/incidents", response_model=schemas.Incident)
def create_incident(incident: schemas.IncidentCreate, db: Session = Depends(get_db),
                    user: User = Depends(fastapi_users.current_user(active=True))
                    ):
    return crud.create_incident(db, incident)


@app.get("/incidents/stream")
async def read_incidents_from_stream(request: Request, db: Session = Depends(get_db),
                                     user: User = Depends(fastapi_users.current_user(active=True))
                                     ):
    incident_generator = incident_event_generator(db, request)
    return EventSourceResponse(incident_generator)
