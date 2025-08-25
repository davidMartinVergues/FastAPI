import uuid

from fastapi import HTTPException,status
from db.db import IAsyncDatabaseRepository
from models import CustomerCreate,Customer, CustomerPlan,CustomerUpdate, Plan
from app.customers.enums.customer_plan import CustomerPlanStatusEnum
from sqlmodel import select



class CustomerRepository(IAsyncDatabaseRepository):
    async def create_customer(self,customer:CustomerCreate):
        if not self.db:
            raise ValueError("Database session not injected")
        
        result = await self.db.execute(select(Customer).where(Customer.email==customer.email))
        
        if result.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use") 
        
        _customer:Customer = Customer.model_validate(customer.model_dump())
        self.db.add(_customer)
        await self.db.flush()
        return _customer


    async def delete_customers(self,customer_id:uuid.UUID):

        # result = session.exec(select(Customer).where(Customer.id ==customer_id))
        #customer = result.one_or_none()
        if not self.db:
            raise ValueError("Database session not injected")
        
        customer = await self.db.get(Customer, customer_id)

        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
        await self.db.delete(customer)
        return {"customer_id":customer_id}

    async def update_customers(self, customer_id:uuid.UUID,customer_data:CustomerUpdate): 
        if not self.db:
            raise ValueError("Database session not injected") 
        customer = await self.db.get(Customer, customer_id)
        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
        # customer.sqlmodel_update(customer_data.model_dump(exclude_unset=True))
        for key, value in customer_data.get_updatable_fields().items():
                setattr(customer, key, value)
                
        self.db.add(customer)
        await self.db.flush()
        return customer


    async def subscribe_customer_to_plan(self,customer_id:uuid.UUID, plan_id:uuid.UUID,plan_status:CustomerPlanStatusEnum):
        if not self.db:
            raise ValueError("Database session not injected")
        
        customer_db : Customer| None = await self.db.get(Customer, customer_id)
        plan_db : Plan | None = await self.db.get(Plan, plan_id)

        if not customer_db or not plan_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer or plan not found")
        
        customer_plan : CustomerPlan = CustomerPlan(customer_id=customer_id,plan_id=plan_id,status=plan_status)

        self.db.add(customer_plan)
        await self.db.flush()

        return  customer_plan
        


