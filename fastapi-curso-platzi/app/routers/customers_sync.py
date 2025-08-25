# from fastapi import HTTPException,status, APIRouter
# from models import Customer, CustomerUpdate,CustomerCreate
# import uuid
# import logging
# from settings.logger_setup import setup_loggers
# from sqlmodel import select
# from db_sync.db import SessionDep

# setup_loggers()
# api_logger = logging.getLogger("api")

# router = APIRouter()


# @router.post('/customers', 
#           status_code=201, 
#           response_model=Customer
#           )
# async def create_customer(customer:CustomerCreate, session:SessionDep):
#     _customer:Customer = Customer.model_validate(customer.model_dump())
#     api_logger.error(f"aqui: {_customer}")
#     session.add(_customer)
#     session.commit()
#     session.refresh(_customer)
    
#     return _customer

# @router.get('/customers', 
#           status_code=201, 
#           response_model=list[Customer]
#           )
# async def list_customers(session:SessionDep):
#     return session.exec(select(Customer)).all()


# @router.get('/customers/{customer_id}', 
#           status_code=201, 
#           response_model=Customer
#           )
# async def get_customers(customer_id:uuid.UUID,session:SessionDep):

#     # result = session.exec(select(Customer).where(Customer.id ==customer_id))
#     #customer = result.one_or_none()
    
#     customer = session.get(Customer, customer_id)
#     if not customer:
#           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
#     return customer

# @router.delete('/customers/{customer_id}')
# async def delete_customers(customer_id:uuid.UUID,session:SessionDep):

#     # result = session.exec(select(Customer).where(Customer.id ==customer_id))
#     #customer = result.one_or_none()
    
#     customer = session.get(Customer, customer_id)
#     if not customer:
#           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
#     session.delete(customer)
#     session.commit()
#     return {"customer_id":customer_id}

# @router.patch('/customers/{customer_id}', status_code=status.HTTP_201_CREATED, response_model=Customer)
# async def update_customers(customer_id:uuid.UUID,customer_data:CustomerUpdate,session:SessionDep):  
#     customer = session.get(Customer, customer_id)
#     if not customer:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
#     # customer.sqlmodel_update(customer_data.model_dump(exclude_unset=True))
#     for key, value in customer_data.get_updatable_fields().items():
#             setattr(customer, key, value)
            
#     session.add(customer)
#     session.commit()
#     session.refresh(customer)
#     return customer
