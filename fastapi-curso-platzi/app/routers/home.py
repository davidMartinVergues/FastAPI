from datetime import datetime
import zoneinfo
from fastapi import APIRouter
from models import Transaction

router = APIRouter()

# timezones
country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima",
}

@router.get('/')
async def home()->dict:
    return {"data":"hello david-2"}

@router.get('/current-time/{iso_code}')
async def time(iso_code:str)->dict:
    timezone_str = country_timezones.get(iso_code.upper())
    if timezone_str is None:
        return {"error": "Invalid country code"}
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"time":datetime.now(tz)}

