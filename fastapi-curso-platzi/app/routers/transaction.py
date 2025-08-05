from fastapi import APIRouter, HTTPException
from sqlmodel import select
from models import Customer, Transaction, TransactionCreate
from db.db import SessionDep as SessionDep_async, transactional


router = APIRouter()


@router.post('/transactions', status_code=201, response_model=Transaction)
@transactional
async def create_transaction(transaction_data:TransactionCreate, session:SessionDep_async):
    
    if not session:
        raise HTTPException(status_code=500, detail="Session not available")
    
    transaction_data_dict = transaction_data.model_dump()
    customer_id = transaction_data_dict.get("customer_id")
    customer = await session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    transaction_db = Transaction.model_validate(transaction_data_dict)
    session.add(transaction_db)
    await session.commit()
    await session.refresh(transaction_db)

    return transaction_db


@router.get('/transactions', response_model=list[Transaction])
async def list_transactions(session:SessionDep_async)->list[Transaction]:
    result = await session.execute(select(Transaction))
    return list(result.scalars().all())

    