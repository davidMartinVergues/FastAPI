from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlmodel import select
from models import Customer, Transaction, TransactionCreate, TransactionResponse
from app.transactions.transactions_service import TransactionsService
from fastapi_restful.cbv import cbv
from fastapi import APIRouter, Request
from fastapi_pagination import Page

router = APIRouter()

class Test(BaseModel):
     name:str

@cbv(router)
class TransactionRouter:
    def __init__(self):
        self.transaction_service = TransactionsService()

    @router.get('/transactions-list',response_model=Page) # si pongo Page[TransactionResponse] se rompe
    async def list_transactions(self, request: Request, test:Test = Depends()
                                )->Page[TransactionResponse]:
        transaction_service = TransactionsService()
        try:
            return await transaction_service.list_transactions()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.post('/transactions', response_model=Transaction, status_code=201)
    async def create_transaction(self, request: Request,tranmsaction_data: TransactionCreate)-> Transaction:
            try:
                return await self.transaction_service.create_transaction(tranmsaction_data)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))