from sqlmodel import select
from sqlalchemy.orm import selectinload
from models import Customer
from db.db import IAsyncDatabaseRepository
from models import Plan, PlanCreate
import logging
import uuid

log_api = logging.getLogger("api")



class PlanRepository(IAsyncDatabaseRepository):
    async def list_plans(self)->list[Plan]:
        """listar transactions"""
        if not self.db:
            raise ValueError("Database session not injected")
        
        plans = await self.db.execute(select(Plan).options(selectinload(Plan._customers))) # type: ignore
        plans = plans.scalars().all()
  
        return list(plans)
    
    async def create_plan(self, plan_data:PlanCreate)->Plan:
        """crear transaction"""
        if not self.db:
            raise ValueError("Database session not injected")
        
        plan_db = Plan.model_validate(plan_data.model_dump())
        log_api.error(F"{plan_db}")
        self.db.add(plan_db)
        await self.db.flush()
        return plan_db
        
        
        


        

        
