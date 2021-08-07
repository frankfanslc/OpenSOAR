from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import SessionLocal

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


@app.get("/users", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.post("/users", response_model=schemas.User, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get(
    "/users/{user_id}/incidents", response_model=List[schemas.Incident], status_code=201
)
def get_incidents_by_user(
    user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return crud.get_user_incidents(db=db, user_id=user_id, skip=skip, limit=limit)


@app.post(
    "/users/{user_id}/incidents", response_model=schemas.Incident, status_code=201
)
def create_incidents_for_user(
    user_id: int, incident: schemas.IncidentCreate, db: Session = Depends(get_db)
):
    return crud.create_user_incident(db=db, incident=incident, user_id=user_id)


@app.get("/incidents", response_model=List[schemas.Incident])
def read_incidents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    incidents = crud.get_incidents(db, skip=skip, limit=limit)
    return incidents
