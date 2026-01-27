from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from services.market_data import get_multiple_ltp
from services.instrument_map import INSTRUMENT_MAP

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    symbols = list(INSTRUMENT_MAP.keys())[:50]  # आत्ता 50 दाखवू (fast load साठी)
    stocks = get_multiple_ltp(symbols)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "stocks": stocks
    })
