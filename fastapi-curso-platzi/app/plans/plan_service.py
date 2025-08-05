from app.plans.plan_repository import PlanRepository
from db.db import with_transaction
from models import Plan, PlanCreate, TransactionCreate



class PlanService:
    def __init__(self):
        self.plan_repo = PlanRepository()
    
    @with_transaction
    async def create_plan(self, plan_data:PlanCreate):
        return await self.plan_repo.create_plan(plan_data)
    
    @with_transaction
    async def list_plan(self):
        return await self.plan_repo.list_plans()
