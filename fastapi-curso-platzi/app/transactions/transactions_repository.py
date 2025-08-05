from sqlmodel import select
from db.db import IAsyncDatabaseRepository
from models import Customer, Transaction, TransactionCreate

class TransactionsRepository(IAsyncDatabaseRepository):
    async def list_transactions(self)->list[Transaction]:
        """listar transactions"""
        if not self.db:
            raise ValueError("Database session not injected")
        
        transactions = await self.db.execute(select(Transaction))

        return list(transactions.scalars().all())
    
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
        
        
        


        

        
