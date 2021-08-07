from sqlalchemy.orm import Session
from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_incidents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Incident).offset(skip).limit(limit).all()


def get_user_incidents(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Incident).filter(models.Incident.owner_id == user_id).offset(skip).limit(limit).all()


def create_user_incident(db: Session, incident: schemas.IncidentCreate, user_id: int):
    db_incident = models.Incident(**incident.dict(), owner_id=user_id)
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident
