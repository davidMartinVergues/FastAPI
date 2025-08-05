from typing import Union

from fastapi import APIRouter, Request, Depends, HTTPException
from .models import EventCreateSchema, EventUpdateSchema, EventModel, EventListSchema 
from decouple import config as decouple_config
from api.db.config import DATABASE_URL

router = APIRouter()



MOCK_DATA = [EventModel(id=1), EventModel(id=2), EventModel(id=3)]

@router.get('/')
def read_events() -> EventListSchema:
    print(DATABASE_URL)
    return EventListSchema(results=MOCK_DATA, count=len(MOCK_DATA))


@router.get("/{event_id}")
def get_event(request: Request, event_id: int, query_params:EventModel  = Depends(EventModel)) -> EventModel:
# def get_event(request: Request, event_id: int, q: str | None = None) -> EventModel:
# def get_event(event_id: int, q : Union[str,None]=None) -> EventModel:
    print(query_params)
    print(request)
    return EventModel(id=event_id)

@router.post("/")
def create_event(payload: EventModel) -> EventModel:
    new_event = EventModel(id=payload.id,page=payload.page)
    MOCK_DATA.append(new_event)
    return new_event

@router.put("/{event_id}")
def update_event(event_id:int, payload:EventUpdateSchema)->EventListSchema:
    event_to_update = next((event for event in MOCK_DATA if event.id == event_id), None)

    if not event_to_update:
        raise HTTPException(status_code=404, detail="Event not found")
    event_to_update.description = payload.description

    return EventListSchema(results=MOCK_DATA, count=len(MOCK_DATA))

