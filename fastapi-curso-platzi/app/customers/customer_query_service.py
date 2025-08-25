import uuid

from fastapi import HTTPException
from db.db import IAsyncDatabaseRepository
from models import CustomerCreate,Customer, CustomerPlan,CustomerUpdate, Plan
from sqlmodel import select
from app.customers.enums.customer_plan import CustomerPlanStatusEnum
from sqlalchemy.orm import selectinload,joinedload
import logging

log_api = logging.getLogger("api")

class CustomerQueryService(IAsyncDatabaseRepository):

    async def list_customers(self):

        result = await self.db.execute(select(Customer)) # type: ignore
        customers: list[Customer] = list(result.scalars().all())
        return customers


    async def get_customers(self,customer_id:uuid.UUID):
        # customer =  await session.get(Customer, customer_id)
        # if not customer:
        #       raise HTTPException(status_code=404, detail="Customer not found")
        # return customer
  
        result = await self.db.execute(select(Customer).where(Customer.id ==customer_id)) # type: ignore
        customer = result.scalar_one_or_none()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer

    async def get_plans_by_customers(self,customer_id:uuid.UUID):
        result = await self.db.execute(# type: ignore
            select(Customer)
            .options(selectinload(Customer.plans))
            .where(Customer.id == customer_id)
        )
        customer_db = result.scalar_one_or_none()
        
        if not customer_db:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        log_api.error(f"este es el customer : {customer_db.plans}")

        return customer_db.plans

    async def get_customer_plans_by_status(self,customer_id:uuid.UUID, status:CustomerPlanStatusEnum):

        if not self.db:
            raise ValueError("Database session not injected")

        result = await self.db.execute(# type: ignore
            select(Plan)
            .join(CustomerPlan)
            .where(
                CustomerPlan.customer_id == customer_id,
                CustomerPlan.status == status
            )
        )

        customer_plans = result.scalars().all()
        return customer_plans
