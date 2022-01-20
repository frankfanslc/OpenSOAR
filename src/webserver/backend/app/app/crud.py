from sqlalchemy.orm import Session, joinedload
from . import models, schemas


def get_incidents(
    db: Session, skip: int = 0, limit: int = 10, query_filter: str = None
):
    if query_filter:
        incidents = (
            db.query(models.IncidentTable)
            .filter(query_filter)
            .options(joinedload(models.IncidentTable.owner))
            .order_by(models.IncidentTable.id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    else:
        incidents = (
            db.query(models.IncidentTable)
            .options(joinedload(models.IncidentTable.owner))
            .order_by(models.IncidentTable.id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    incidents = [
        {**incident.__dict__, "owner": incident.owner} for incident in incidents
    ]
    total = db.query(models.IncidentTable).count()
    return {"incidents": incidents, "total": total}


def get_user_incidents(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    incidents = (
        db.query(models.IncidentTable)
        .filter(models.IncidentTable.owner_id == user_id)
        .options(joinedload(models.IncidentTable.owner))
        .order_by(models.IncidentTable.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    incidents = [
        {**incident.__dict__, "owner": incident.owner} for incident in incidents
    ]
    total = db.query(models.IncidentTable).count()
    return {"incidents": incidents, "total": total}


def create_incident(db: Session, incident: schemas.IncidentCreate):
    db_incident = models.IncidentTable(**incident.dict())
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return


def read_users(db: Session):
    return db.query(models.UserTable).all()


def get_setting(db: Session, attribute: str = None):
    if attribute:
        return (
            db.query(models.SettingsTable)
            .filter(models.SettingsTable.setting == attribute)
            .first()
        )
    else:
        return db.query(models.SettingsTable).all()


def set_setting(db: Session, attribute: str, value: str):
    setting = (
        db.query(models.SettingsTable)
        .filter(models.SettingsTable.setting == attribute)
        .first()
    )
    if setting:
        setting.value = value
        db.commit()
    else:
        setting = models.SettingsTable(
            **(schemas.SettingCreate(setting=attribute, value=value).dict())
        )
        db.add(setting)
        db.commit()
    return db.refresh(setting)
