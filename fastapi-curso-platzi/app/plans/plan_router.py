from fastapi import APIRouter, HTTPException
from sqlmodel import select
from models import Customer, Plan, PlanCreate, Transaction, TransactionCreate
from app.transactions.transactions_service import TransactionsService
from fastapi_restful.cbv import cbv
from fastapi import APIRouter, Request
from app.plans.plan_service import PlanService


router = APIRouter()

@cbv(router)
class PlanRouter:
    def __init__(self):
        self.plan_service = PlanService()

    @router.get('/plans-list', response_model=list[Plan])
    async def list_plans(self, request: Request)->list[Plan]:
        try:
            return await self.plan_service.list_plan()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.post('/plans', response_model=Plan, status_code=201)
    async def create_plann(self, request: Request,plan_data: PlanCreate)-> Plan:
            try:
                return await self.plan_service.create_plan(plan_data)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))