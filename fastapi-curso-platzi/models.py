from pydantic import BaseModel,EmailStr
import uuid
from sqlmodel import SQLModel,Field, Relationship

class CustomerBase(SQLModel):
    name : str | None = Field(default= None, max_length=250)
    age : int | None = Field(default= None, gt=0)
    email : EmailStr| None = Field(default= None)
    description: str | None = Field(default=None)

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
    _transactions : list["Transaction"] = Relationship(back_populates="_customer")

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

    def updatbale_fields(self):
        updatblae_fields={
            "name",
            "email"
        }
        return {k:v for k,v in self.model_dump().items() if getattr(self,k) and k in updatblae_fields}