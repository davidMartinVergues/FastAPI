import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlmodel import SQLModel
from settings.settings import settings
from models import Customer
from app.main_async import app
from db.db import get_session

engine_test = create_async_engine(
    settings.database.url_async_test,
    echo=False,  # Disable for cleaner test output
    future=True,
    connect_args={"check_same_thread": False}
)

async_session_test = async_sessionmaker(
    engine_test, 
    expire_on_commit=False,
    class_=AsyncSession
)

@pytest.fixture(scope="session")
async def session():
    """Create a fresh database session for all test"""
    async with engine_test.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    
    async with async_session_test() as session:
        # Establecer la sesión en el contexto global para @with_transaction
        from db.db import set_current_session
        set_current_session(session)
        yield session
    
    async with engine_test.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

@pytest.fixture(scope="session")
async def client(session: AsyncSession):
    """Create HTTP client with dependency override"""
    
    async def override_get_session():
        yield session
    
    # Override both the dependency and disable lifespan for tests
    app.dependency_overrides[get_session] = override_get_session
    
    # Create a new app instance without lifespan for tests
    from fastapi import FastAPI
    test_app = FastAPI()
    
    # Copy all routes from the original app
    test_app.include_router(app.router)
    test_app.dependency_overrides = app.dependency_overrides.copy()
    
    from httpx import ASGITransport
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        yield async_client
    
    app.dependency_overrides.clear()

@pytest.fixture
async def customer(session: AsyncSession):
    """Create a test customer"""
    customer = Customer(
        name="Test Customer",
        age=25,
        email="test@example.com",
        description="Test description"
    )
    session.add(customer)
    await session.commit()
    await session.refresh(customer)
    return customer
