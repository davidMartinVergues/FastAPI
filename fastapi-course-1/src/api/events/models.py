from fastapi import Query
# from pydantic import SQLModel, Field
from typing import List, Optional

from sqlmodel import SQLModel, Field


class EventCreateSchema(SQLModel):
    id:int
    page:str

class EventUpdateSchema(SQLModel):
    description:str

# class EventSchema(SQLModel):
    # id : int
    # page: Optional[str] = Field(
    #     default=None,
    #     title="Event page",
    #     description="The URL or slug of the event page.",
    #     max_length=200,
    #     examples=["event-123"]
    # )
    # description: Optional[str] = Field(
    #         default=None,
    #         title="Event descriptoin",
    #         description="description event",
    #         max_length=200,
    #         examples=["description-1"]
    #     )

# class EventListSchema(SQLModel):
#     results : List[EventSchema]
#     count : int