from app.transactions.transactions_repository import TransactionsRepository
from db.db import with_transaction
from models import Transaction, TransactionCreate, TransactionResponse
from fastapi_pagination import Page
import logging

log_api = logging.getLogger("api")


class TransactionsService:
    def __init__(self):
        self.transactions_repo = TransactionsRepository()
    
    @with_transaction
    async def create_transaction(self, transaction_data:TransactionCreate):
        return await self.transactions_repo.create_transaction(transaction_data)
    
    @with_transaction
    async def list_transactions(self)->Page[TransactionResponse]:
        transactions : Page[Transaction] = await self.transactions_repo.list_transactions()
        return Page(
          items=[TransactionResponse.from_transaction(item) for item in transactions.items],
          total=transactions.total,
          page=transactions.page,
          size=transactions.size,
          pages=transactions.pages
        )
