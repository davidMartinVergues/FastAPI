import uuid
from fastapi import APIRouter, HTTPException, Query, Request,status
from fastapi_restful.cbv import cbv
from .customer_service import CustomerService
from models import Customer, CustomerUpdate,CustomerCreate, Plan, PlanResponse,CustomerPlan
from app.customers.enums.customer_plan import CustomerPlanStatusEnum

router = APIRouter()

@cbv(router)
class CustomerRouter:
    def __init__(self):
        self.customer_service = CustomerService()
    
    @router.post('/customers', status_code=201, response_model=Customer)
    async def create_customer(self, request: Request,customer:CustomerCreate)->Customer:

        try:
            return  await self.customer_service.create_customer(customer)
        except HTTPException:
            raise # Re-lanza HTTPException tal como está (mantiene status_code original)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal server error")

    @router.post('/customers/{customer_id}/plans/{plan_id}', status_code=201, response_model=CustomerPlan)
    async def add_customer_to_plan(self, request: Request,customer_id:uuid.UUID, plan_id:uuid.UUID, plan_status: CustomerPlanStatusEnum = Query(default=CustomerPlanStatusEnum.ACTIVE)):

        try:
            return  await self.customer_service.subscribe_customer_to_plan(customer_id, plan_id,plan_status)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.patch('/customers/{customer_id}', status_code=status.HTTP_201_CREATED, response_model=Customer)
    async def update_customers(self,customer_id:uuid.UUID,customer_data:CustomerUpdate):  
            try:
                return await self.customer_service.update_customer(customer_id,customer_data)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
            
    @router.delete('/customers/{customer_id}')
    async def delete_customers(self, customer_id:uuid.UUID):
            try:
                return await self.customer_service.delete_customers(customer_id)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

    @router.get('/customers', status_code=201, response_model=list[Customer])
    async def list_customers(self):
            try:
                return await self.customer_service.list_customers()
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

    @router.get('/customers/{customer_id}', status_code=200, response_model=Customer)
    async def get_customers(self, customer_id:uuid.UUID):
            try:
                return await self.customer_service.get_customers(customer_id)
            except HTTPException as e:
                 raise e 
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

    @router.get('/customers/{customer_id}/plans', status_code=201, response_model=list[Plan])
    async def get_customers_plans(self, customer_id:uuid.UUID):
            try:
                return await self.customer_service.get_plans_by_customers(customer_id)
            
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

    @router.get('/customers/{customer_id}/plans/{status}', status_code=201, response_model=list[Plan])
    async def get_customers_plans_by_status(self, customer_id:uuid.UUID, status:CustomerPlanStatusEnum):
            try:
                return await self.customer_service.get_customer_plans_by_status(customer_id,status)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

