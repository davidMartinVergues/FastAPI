from typing import Union

from fastapi import APIRouter, Request, Depends, HTTPException
from .models import EventSchema, EventListSchema, EventCreateSchema, EventUpdateSchema
from decouple import config as decouple_config
from api.db.config import DATABASE_URL

router = APIRouter()



MOCK_DATA = [EventSchema(id=1), EventSchema(id=2), EventSchema(id=3)]

@router.get('/')
def read_events() -> EventListSchema:
    print(DATABASE_URL)
    return EventListSchema(results=MOCK_DATA, count=len(MOCK_DATA))


@router.get("/{event_id}")
def get_event(request: Request, event_id: int, query_params:EventSchema  = Depends(EventSchema)) -> EventSchema:
# def get_event(request: Request, event_id: int, q: str | None = None) -> EventSchema:
# def get_event(event_id: int, q : Union[str,None]=None) -> EventSchema:
    print(query_params)
    print(request)
    return EventSchema(id=event_id)

@router.post("/")
def create_event(payload: EventCreateSchema) -> EventSchema:
    new_event = EventSchema(id=payload.id,page=payload.page)
    MOCK_DATA.append(new_event)
    return new_event

@router.put("/{event_id}")
def update_event(event_id:int, payload:EventUpdateSchema)->EventListSchema:
    event_to_update = next((event for event in MOCK_DATA if event.id == event_id), None)

    if not event_to_update:
        raise HTTPException(status_code=404, detail="Event not found")
    event_to_update.description = payload.description

    return EventListSchema(results=MOCK_DATA, count=len(MOCK_DATA))

