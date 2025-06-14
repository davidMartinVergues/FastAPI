from fastapi import Query
from pydantic import BaseModel, Field
from typing import List, Optional


class EventCreateSchema(BaseModel):
    id:int
    page:str

class EventUpdateSchema(BaseModel):
    description:str

class EventSchema(BaseModel):
    id : int
    page: Optional[str] = Field(
        default=None,
        title="Event page",
        description="The URL or slug of the event page.",
        max_length=200,
        examples=["event-123"]
    )
    description: Optional[str] = Field(
            default=None,
            title="Event descriptoin",
            description="description event",
            max_length=200,
            examples=["description-1"]
        )

class EventListSchema(BaseModel):
    results : List[EventSchema]
    count : int