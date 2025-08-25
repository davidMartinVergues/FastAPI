from typing import AsyncGenerator, Annotated, Any
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from fastapi import Depends
from settings.settings import settings
from sqlmodel import SQLModel
import logging
from functools import wraps
from contextvars import ContextVar
from contextlib import asynccontextmanager


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

# Context variable para almacenar la sesión actual
current_session: ContextVar[AsyncSession | None] = ContextVar("current_session", default=None)


# =============================================================================
# SESSION CONTEXT MANAGEMENT (inspirado en sistema IATI)
# =============================================================================

def get_current_session() -> AsyncSession | None:
    """Obtiene la sesión actual del contexto"""
    return current_session.get()


def set_current_session(session: AsyncSession) -> None:
    """Establece la sesión en el contexto"""
    current_session.set(session)


def clear_current_session() -> None:
    """Limpia la sesión del contexto"""
    current_session.set(None)


async def create_all_tables_async():
    """este método permite la creación de todas las tablas en base a ModelSQL (si es q no estan creadas)"""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    print("✅ Tables created successfully")

# =============================================================================
# SESSION MANAGERS
# =============================================================================

@asynccontextmanager
async def session_manager():
    """
    Context manager transaccional inspirado en IATI pero async.
    Provee un scope transaccional alrededor de una serie de operaciones.
    """
    existing_session = get_current_session()
    if existing_session is not None:
        yield existing_session
        return

    async with async_session_maker() as session:
        try:
            set_current_session(session)
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            clear_current_session()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Generador de sesión para dependencia de FastAPI"""
    async with session_manager() as session:
        yield session

# =============================================================================
# REPOSITORY INJECTION SYSTEM (inspirado en IATI)
# =============================================================================

class IAsyncDatabaseRepository:
    """Interface base para repositorios con acceso a DB async"""
    def __init__(self):
        self.db: AsyncSession | None = None

    def set_session(self, db: AsyncSession):
        """Inyecta la sesión en el repositorio"""
        self.db = db


async def _inject_session_into_instance(instance: Any, session: AsyncSession) -> None:
    """Inyecta sesión en repositorios con acceso a base de datos"""
    for attr_name in dir(instance):
        attr = getattr(instance, attr_name)
        if isinstance(attr, IAsyncDatabaseRepository):
            attr.set_session(session)


# =============================================================================
# TRANSACTION DECORATORS
# =============================================================================

def with_transaction(func):
    """
    Decorator que provee un scope transaccional alrededor de un use case.
    Inspirado en el sistema IATI pero adaptado para async.
    Inyecta automáticamente sesiones en repositorios.
    """
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        async with session_manager() as session:
            await _inject_session_into_instance(self, session)
            return await func(self, *args, **kwargs)
    return wrapper

SessionDep = Annotated[AsyncSession, Depends(get_session)]

