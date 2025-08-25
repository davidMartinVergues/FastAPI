from app.transactions.transactions_repository import TransactionsRepository
from db.db import with_transaction
from models import TransactionCreate



class TransactionsService:
    def __init__(self):
        self.transactions_repo = TransactionsRepository()
    
    @with_transaction
    async def create_transaction(self, transaction_data:TransactionCreate):
        return await self.transactions_repo.create_transaction(transaction_data)
    
    @with_transaction
    async def list_transactions(self,page,size):
        return await self.transactions_repo.list_transactions(page,size)
