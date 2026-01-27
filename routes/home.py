from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from services.market_data import get_multiple_ltp

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    symbols = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ITC", "SBIN"]
    stocks = get_multiple_ltp(symbols)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "stocks": stocks
    })
