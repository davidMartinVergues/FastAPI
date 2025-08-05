from fastapi import FastAPI,HTTPException
from datetime import datetime
import zoneinfo
from models import Customer,Transaction, Invoice,CustomerCreate
import uuid
from db.db import create_all_tables_async ,SessionDep as SessionDep_async
from contextlib import asynccontextmanager
import logging
from settings.logger_setup import setup_loggers
from sqlmodel import select
from app.routers.customers_async import router as customers_router
from app.routers.transaction  import router as transactions_router
from app.routers.invoice import router as invoices_router
from app.routers.home import router as home_router


setup_loggers()

api_logger = logging.getLogger("api")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    await create_all_tables_async()
    api_logger.warning("init method for db ASINCRONO")
    # create_all_tables(app)
    # api_logger.info("init method for db SINCRONO")
    yield
    # shutdown
    # some clean up code
    api_logger.info("shutdown method for db")

app = FastAPI(lifespan=lifespan,root_path="/api/async")

app.include_router(customers_router, tags=["customers_async"], prefix="/v1")
app.include_router(transactions_router, tags=["transactions"], prefix="/v1")
app.include_router(invoices_router, tags=["invoices"], prefix="/v1")
app.include_router(home_router, tags=["home"], prefix="/v1")




