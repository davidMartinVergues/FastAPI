from pydantic import BaseModel,EmailStr, field_validator
import uuid
from sqlmodel import SQLModel,Field, Relationship
from app.customers.enums.customer_plan import CustomerPlanStatusEnum
# Definir CustomerPlan PRIMERO
class CustomerPlan(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    plan_id: uuid.UUID = Field(foreign_key="plan.id")
    customer_id: uuid.UUID  = Field(foreign_key="customer.id")
    status:CustomerPlanStatusEnum = Field(default=CustomerPlanStatusEnum.ACTIVE)

class CustomerBase(SQLModel):
    name : str | None = Field(default= None, max_length=250)
    age : int | None = Field(default= None, gt=0)
    email : EmailStr| None = Field(default= None)
    description: str | None = Field(default=None)

    '''
    no vamos a hacer validaciones q requieran la bbdd en el modelo debemos hacerlo en el use_case o service
    '''
    # @field_validator("email")
    # @classmethod
    # def validate_email(cls,value):

    #     return value
        

    def get_updatable_fields(self)->dict:
        updatable_fields={
            "name",
            "age",
            "email",
            "description"
        }
        return {k:v for k,v in self.model_dump().items() if getattr(self, k) and k in updatable_fields}


class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass


class Customer(CustomerBase, table=True):
    id : uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    _transactions : list["Transaction"] = Relationship(back_populates="_customer", cascade_delete=True)
    plans: list["Plan"] = Relationship(back_populates="_customers", link_model=CustomerPlan)

class CustomerResponse(BaseModel):
    id: uuid.UUID
    name: str | None = None
    email: EmailStr | None = None

    @classmethod
    def from_customer(cls,customer: Customer) -> 'CustomerResponse':
          return cls(
              id=customer.id,
              name=customer.name,
              email=customer.email,
          )

class TransactionBase(SQLModel):
    amount : float 
    description: str

class Transaction(TransactionBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    customer_id: uuid.UUID = Field(foreign_key="customer.id")
    _customer: Customer = Relationship(back_populates="_transactions")

class TransactionCreate(TransactionBase):
    customer_id: uuid.UUID = Field(foreign_key="customer.id")
    
class Invoice(BaseModel):
    id:int 
    customer : Customer
    transactions : list[Transaction]
        
    @property
    def total(self):
        return sum(transaction.amount for transaction in self.transactions)
    

class Users(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(index=True)

class UsersUpdate(BaseModel):
    id: uuid.UUID|None = None
    name: str |None = None
    email: str|None = None

    def updatable_fields(self):
        updatable_fields = {
            "name",
            "email"
        }
        return {k: v for k, v in self.model_dump().items() if getattr(self, k) and k in updatable_fields}
    
# Base class para Plan
class PlanBase(SQLModel):
    name: str | None = Field(default=None, max_length=250)
    price: float | None = Field(default=None, gt=0)
    description: str | None = Field(default=None)

    def get_updatable_fields(self) -> dict:
        updatable_fields = {
            "name",
            "price", 
            "description"
        }
        return {k: v for k, v in self.model_dump().items() if getattr(self, k) and k in updatable_fields}


class PlanCreate(PlanBase):
    pass


class PlanUpdate(PlanBase):
    pass  # ← Todos opcionales al actualizar


class Plan(PlanBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    _customers: list['Customer'] = Relationship(back_populates="plans", link_model=CustomerPlan) 
    # Los campos que empiezan con _ son considerados privados por Pydantic y no se incluyen en la serialización por defecto.

class PlanResponse(BaseModel):
    id: uuid.UUID
    name:str | None = None
    price: float | None = None
    description: str | None = None
    customers: list[CustomerResponse] = []

    @classmethod
    def from_plan(cls,plan: Plan) -> 'PlanResponse':
          return cls(
              id=plan.id,
              name=plan.name,
              price=plan.price,
              description=plan.description,
              customers=[CustomerResponse.from_customer(c) for c in plan._customers]
          )

class TransactionResponse(SQLModel):
    id: uuid.UUID
    amount:float | None = None
    description: str | None = None
    customer: CustomerResponse | None = None

    @classmethod
    def from_transaction(cls,transaction: Transaction) -> 'TransactionResponse':
          return cls(
            id=transaction.id,
            amount=transaction.amount,
            description=transaction.description,
            customer=CustomerResponse.from_customer(transaction._customer)
          )

