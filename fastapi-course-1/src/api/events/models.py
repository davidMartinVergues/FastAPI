from fastapi import Query
# from pydantic import SQLModel, Field
from typing import List, Optional

from sqlmodel import SQLModel, Field

import uuid

class EventModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    page: Optional[str] = Field(
        default="",
        title="Event page",
        description="The URL or slug of the event page.",
        max_length=200,
    )
    description: Optional[str] = Field(
            default="",
            title="Event description",
            description="description event",
            max_length=200,
        )

class EventCreateSchema(SQLModel):
    page:str
    description: Optional[str] = Field(default="")

class EventUpdateSchema(SQLModel):
    description:str


class EventListSchema(SQLModel):
    results : List[EventModel]
    count : int