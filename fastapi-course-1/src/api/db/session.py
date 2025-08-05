
import sqlmodel
from .config import DATABASE_URL
from sqlmodel import SQLModel
from api.events.models import EventModel
if DATABASE_URL == "database url not found":
    raise NotImplementedError("DATABASE_URL needs to be set on .env file.")

engine = sqlmodel.create_engine(DATABASE_URL, echo=True)

def init_db():
    print("creating db")
    SQLModel.metadata.create_all(engine)
