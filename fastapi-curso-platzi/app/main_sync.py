from fastapi import FastAPI
from datetime import datetime
import zoneinfo
from models import Transaction, Invoice
import logging
from settings.logger_setup import setup_loggers
from db_sync.db import  create_all_tables
from app.routers.customers_sync import router as customers_router
from app.routers.transaction import router as transactions_router
from app.routers.invoice import router as invoices_router
from app.routers.home import router as home_router

setup_loggers()

api_logger = logging.getLogger("api")



app = FastAPI(lifespan=create_all_tables,root_path="/api") # pyright: ignore[reportArgumentType]

app.include_router(customers_router, tags=["customers"], prefix="/v1")
app.include_router(transactions_router, tags=["transactions"], prefix="/v1")
app.include_router(invoices_router, tags=["invoices"], prefix="/v1")
app.include_router(home_router, tags=["home"], prefix="/v1")