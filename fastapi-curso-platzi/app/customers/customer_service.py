import uuid

from fastapi import HTTPException,status
from db.db import with_transaction
from .customer_command_repository import CustomerRepository
from .customer_query_service import CustomerQueryService
from models import Customer, CustomerUpdate,CustomerCreate

from app.customers.enums.customer_plan import CustomerPlanStatusEnum


class CustomerService:
    def __init__(self):
        self.customer_command_repo = CustomerRepository()
        self.customer_query_service = CustomerQueryService()
    
    @with_transaction
    async def create_customer(self, customer:CustomerCreate):
        return await self.customer_command_repo.create_customer(customer)
    
    @with_transaction
    async def update_customer(self,customer_id:uuid.UUID,customer_data:CustomerUpdate):
        return await self.customer_command_repo.update_customers(customer_id, customer_data)
    
    @with_transaction
    async def delete_customers(self,customer_id:uuid.UUID):
        return await self.customer_command_repo.delete_customers(customer_id)
   
    @with_transaction
    async def subscribe_customer_to_plan(self,customer_id:uuid.UUID, plan_id:uuid.UUID,plan_status:CustomerPlanStatusEnum):
        return await self.customer_command_repo.subscribe_customer_to_plan(customer_id,plan_id,plan_status)
    
    @with_transaction
    async def list_customers(self):
        return await self.customer_query_service.list_customers()
    
    @with_transaction
    async def get_customers(self,customer_id:uuid.UUID):
        return await self.customer_query_service.get_customers(customer_id)

    @with_transaction
    async def get_plans_by_customers(self,customer_id:uuid.UUID):
        return await self.customer_query_service.get_plans_by_customers(customer_id)

    @with_transaction
    async def get_customer_plans_by_status(self,customer_id:uuid.UUID,status:CustomerPlanStatusEnum):
        return await self.customer_query_service.get_customer_plans_by_status(customer_id,status)
   

