from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from services.scanner_engine import scan_all_stocks

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    breakout, intraday = scan_all_stocks()

    def row(stock):
        color = "lime" if stock["percent"] >= 0 else "red"
        return f"""
        <tr>
            <td>{stock['symbol']}</td>
            <td>₹ {stock['ltp']}</td>
            <td style='color:{color}'>{stock['percent']}%</td>
            <td>{stock['signal']}%</td>
            <td>{stock['time']}</td>
        </tr>
        """

    breakout_rows = "".join([row(s) for s in breakout])
    intraday_rows = "".join([row(s) for s in intraday])

    return f"""
    <html>
    <body style="background:#0b0b0b;color:white;font-family:sans-serif">

    <h1 style="text-align:center;font-size:48px">SPTraders</h1>

    <h2>BREAKOUT STOCK</h2>
    <table width="100%" border="1" cellpadding="8">
    <tr><th>SYMBOL</th><th>LTP</th><th>%</th><th>SIGNAL%</th><th>TIME</th></tr>
    {breakout_rows}
    </table>

    <h2 style="margin-top:40px">INTRADAY BOOST</h2>
    <table width="100%" border="1" cellpadding="8">
    <tr><th>SYMBOL</th><th>LTP</th><th>%</th><th>SIGNAL%</th><th>TIME</th></tr>
    {intraday_rows}
    </table>

    </body>
    </html>
    """
