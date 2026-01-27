from fastapi import APIRouter
from services.market_data import get_live_data

router = APIRouter(prefix="/api")

@router.get("/stocks")
def stocks():
    return get_live_data()
