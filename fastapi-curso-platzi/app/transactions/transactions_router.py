from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select
from models import Customer, Transaction, TransactionCreate
from app.transactions.transactions_service import TransactionsService
from fastapi_restful.cbv import cbv
from fastapi import APIRouter, Request
from fastapi_pagination import Page

router = APIRouter()

@cbv(router)
class TransactionRouter:
    def __init__(self):
        self.transaction_service = TransactionsService()

    @router.get('/transactions-list')
    async def list_transactions(self, request: Request,page=1,size=10
                                ) -> Page[Transaction]:
        transaction_service = TransactionsService()
        try:
            return await transaction_service.list_transactions(page,size)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.post('/transactions', response_model=Transaction, status_code=201)
    async def create_transaction(self, request: Request,tranmsaction_data: TransactionCreate)-> Transaction:
            try:
                return await self.transaction_service.create_transaction(tranmsaction_data)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))