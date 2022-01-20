from typing import Dict, Union, List

from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from .. import schemas


def get_incidents_router(app):
    router = APIRouter()

    @router.get(
        "/incidents", response_model=Dict[str, Union[List[schemas.IncidentRead], int]]
    )
    def read_incidents(
        skip: int = 0,
        limit: int = 10,
        query_filter: str = None,
        db: Session = Depends(get_db),
        user: User = Depends(fastapi_users.current_user(active=True)),
    ):
        return crud.get_incidents(db, skip=skip, limit=limit, query_filter=query_filter)

    @router.post("/incidents", response_model=schemas.Incident)
    def create_incident(
        incident: schemas.IncidentCreate,
        db: Session = Depends(get_db),
        user: User = Depends(fastapi_users.current_user(active=True)),
    ):
        return crud.create_incident(db, incident)

    @router.get("/incidents/stream")
    async def read_incidents_from_stream(
        request: Request,
        db: Session = Depends(get_db),
        user: User = Depends(fastapi_users.current_user(active=True)),
    ):
        incident_generator = incident_event_generator(db, request)
        return EventSourceResponse(incident_generator)
