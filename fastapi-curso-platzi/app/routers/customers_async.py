from fastapi import HTTPException,status, APIRouter
from models import Customer, CustomerUpdate,CustomerCreate
import uuid
import logging
from settings.logger_setup import setup_loggers
from sqlmodel import select
from db.db import SessionDep as SessionDep_async

setup_loggers()

api_logger = logging.getLogger("api")

router = APIRouter()


@router.post('/customers', 
          status_code=201, 
          response_model=Customer
          )
async def create_customer(customer:CustomerCreate, session:SessionDep_async):
    _customer:Customer = Customer.model_validate(customer.model_dump())
    session.add(_customer)
    await session.commit()
    await session.refresh(_customer)

    
    return _customer

@router.get('/customers', 
          status_code=201, 
          response_model=list[Customer]
          )
async def list_customers(session:SessionDep_async):
    result = await session.execute(select(Customer))
    customers: list[Customer] = list(result.scalars().all())
    return customers


@router.get('/customers/{customer_id}', 
          status_code=201, 
          response_model=Customer
          )
async def get_customers(customer_id:uuid.UUID,session:SessionDep_async):
    # customer =  await session.get(Customer, customer_id)
    # if not customer:
    #       raise HTTPException(status_code=404, detail="Customer not found")
    # return customer
    result = await session.execute(select(Customer).where(Customer.id ==customer_id))
    customer = result.scalar_one_or_none()
    if not customer:
          raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.delete('/customers/{customer_id}')
async def delete_customers(customer_id:uuid.UUID,session:SessionDep_async):

    # result = session.exec(select(Customer).where(Customer.id ==customer_id))
    #customer = result.one_or_none()
    
    customer = await session.get(Customer, customer_id)

    if not customer:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    await session.delete(customer)
    await session.commit()
    return {"customer_id":customer_id}

@router.patch('/customers/{customer_id}', status_code=status.HTTP_201_CREATED, response_model=Customer)
async def update_customers(customer_id:uuid.UUID,customer_data:CustomerUpdate,session:SessionDep_async):  
    customer = await session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    # customer.sqlmodel_update(customer_data.model_dump(exclude_unset=True))
    for key, value in customer_data.get_updatable_fields().items():
            setattr(customer, key, value)
            
    session.add(customer)
    await session.commit()
    await session.refresh(customer)
    return customer
