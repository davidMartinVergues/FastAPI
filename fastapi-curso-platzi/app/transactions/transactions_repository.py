from sqlmodel import select
from db.db import IAsyncDatabaseRepository
from models import Customer, Transaction, TransactionCreate
from sqlalchemy import func
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Query
from fastapi_pagination import Page,Params
from sqlalchemy.orm import selectinload,joinedload
import logging

log_api = logging.getLogger("api")
class TransactionsRepository(IAsyncDatabaseRepository):
    async def list_transactions(self)->Page[Transaction]:
        """listar transactions"""
        if not self.db:
            raise ValueError("Database session not injected")
        
        query = select(Transaction).options(selectinload(Transaction._customer)) # type: ignore
        return  await paginate(self.db, query)
    
    async def create_transaction(self, transaction_data:TransactionCreate):
        """crear transaction"""
        if not self.db:
            raise ValueError("Database session not injected")
        
        transaction_data_dict = transaction_data.model_dump()
        customer_id = transaction_data_dict.get("customer_id")

        customer_obj = await self.db.get(Customer, customer_id)
        if not customer_obj:
            raise ValueError("Customer not found")
        
        transaction_db = Transaction.model_validate(transaction_data_dict)

        self.db.add(transaction_db)

        return transaction_db
        
        
        


        

        
