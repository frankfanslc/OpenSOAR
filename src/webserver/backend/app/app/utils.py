import asyncio

from fastapi import Request
from sqlalchemy.orm import Session

from .crud import get_incidents

incident_stream_delay = 5  # second
incident_stream_retry_timeout = 30000  # millisecond


async def incident_event_generator(db: Session, request: Request):
    last_incident_id = 0
    while True:
        if await request.is_disconnected():
            break
        incidents = get_incidents(db, skip=last_incident_id)
        if incidents and last_incident_id != incidents[-1].id:
            yield {
                "event": "update",
                "retry": incident_stream_retry_timeout,
                "data": [dict(incident) for incident in incidents],
            }
            last_incident_id = incidents[-1].id
        await asyncio.sleep(incident_stream_delay)
