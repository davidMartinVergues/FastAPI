import logging

from fastapi import Depends
from sqlmodel import Session,create_engine, SQLModel
from settings.settings import settings
from fastapi import FastAPI
from typing import Annotated

log_api = logging.getLogger("api")

## :::::::::::::::::::::::::::::::::                      
##. CONEXION A DDBB SINCRONA 
##:::::::::::::::::::::::::::::

# Crear motor sync
engine = create_engine(settings.database.url_sync)

def create_all_tables(app:FastAPI):
    SQLModel.metadata.create_all(engine) # crea todas las tablas
    yield # cedemos el control de esa funcionalidad a FastAPI y cuando cerremos la app se ejecuta lo q hay depsués del yiels y como no hay nada se cierra

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]