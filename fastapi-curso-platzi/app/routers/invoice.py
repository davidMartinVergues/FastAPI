from fastapi import APIRouter
from models import Invoice

router = APIRouter()

@router.post('/invoices', status_code=201)
async def create_incvoice(invoice:Invoice)->dict:
    return {"data":invoice.total}
