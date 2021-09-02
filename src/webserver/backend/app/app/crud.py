from sqlalchemy.orm import Session, joinedload
from . import models, schemas


def get_incidents(db: Session, skip: int = 0, limit: int = 10, query_filter: str = None):
    if query_filter:
        incidents = db.query(models.Incident) \
            .filter(query_filter) \
            .options(joinedload(models.Incident.owner)) \
            .order_by(models.Incident.id) \
            .offset(skip) \
            .limit(limit) \
            .all()
    else:
        incidents = db.query(models.Incident)\
            .options(joinedload(models.Incident.owner))\
            .order_by(models.Incident.id)\
            .offset(skip)\
            .limit(limit)\
            .all()
    incidents = [{**incident.__dict__, "owner": incident.owner} for incident in incidents]
    total = db.query(models.Incident).count()
    return {"incidents": incidents, "total": total}


def get_user_incidents(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    incidents = db.query(models.Incident) \
        .filter(models.Incident.owner_id == user_id) \
        .options(joinedload(models.Incident.owner)) \
        .order_by(models.Incident.id) \
        .offset(skip) \
        .limit(limit) \
        .all()
    incidents = [{**incident.__dict__, "owner": incident.owner} for incident in incidents]
    total = db.query(models.Incident).count()
    return {"incidents": incidents, "total": total}


def create_incident(db: Session, incident: schemas.IncidentCreate):
    db_incident = models.Incident(**incident.dict())
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return


def read_users(db):
    return db.query(models.User).all()


# def modify_user(user_id, values, db):
#     db.update(models.User).where(models.User.id == user_id).values(**values)
#     return
