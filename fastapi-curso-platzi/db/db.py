from typing import AsyncGenerator, Annotated
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from fastapi import Depends
from settings.settings import settings
from sqlmodel import SQLModel
import logging
from functools import wraps
from contextvars import ContextVar
from sqlalchemy.orm import Session


log_api = logging.getLogger("api")

## :::::::::::::::::::::::::::::::::                      
##. CONEXION A DDBB ASYNCRONA 
##:::::::::::::::::::::::::::::

# Crear motor async
engine = create_async_engine(
    settings.database.url_async,
    echo=settings.database.ECHO,
    pool_size=settings.database.POOL_SIZE,
    max_overflow=settings.database.MAX_OVERFLOW,
    pool_timeout=30,
    pool_pre_ping=True,
)

# Crear sessionmaker para sesiones asíncronas
async_session_maker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

current_session: ContextVar[Session | None] = ContextVar("current_session", default=None)


async def create_all_tables_async():
    """este método permite la creación de todas las tablas en base a ModelSQL (si es q no estan creadas)"""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    print("✅ Tables created successfully")

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """devuelve una session con manejo de errores"""
    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            current_session.set(None)
            await session.close()

def transactional(func):
    """
    Decorator que engloba la función en una transacción SQL.
    - Requiere que la sesión sea inyectada en kwargs
    - Hace commit automático si todo sale bien
    - Hace rollback automático si hay alguna excepción
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Verificar si hay una sesión inyectada en los kwargs
        session = kwargs.get('session')
        
        if not session:
            raise ValueError("transactional decorator requires 'session' to be injected in kwargs")
        
        try:
            result = await func(*args, **kwargs)
            await session.commit()
            return result
        except Exception:
            await session.rollback()
            raise
    return wrapper



SessionDep = Annotated[AsyncSession, Depends(get_session)]

