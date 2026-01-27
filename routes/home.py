from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from services.scanner_engine import scan_all_stocks

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    breakout, intraday = scan_all_stocks()

    def row(stock):
        color = "lime" if stock["percent"] >= 0 else "red"

        tv_link = f"https://www.tradingview.com/chart/?symbol=NSE:{stock['symbol']}"

        return f"""
        <tr>
            <td>
                <a href="{tv_link}" target="_blank" style="color:cyan;text-decoration:none;font-weight:bold">
                    {stock['symbol']}
                </a>
            </td>
            <td>₹ {stock['ltp']}</td>
            <td style='color:{color};font-weight:bold'>{stock['percent']}%</td>
            <td>{stock['signal']}%</td>
            <td>{stock['time']}</td>
        </tr>
        """

    breakout_rows = "".join([row(s) for s in breakout])
    intraday_rows = "".join([row(s) for s in intraday])

    return f"""
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>

    <body style="background:#0b0b0b;color:white;font-family:sans-serif;padding:10px">

    <h1 style="text-align:center;font-size:52px;font-weight:bold;color:#00ffcc;margin-bottom:20px">
        SPTraders
    </h1>

    <div style="background:#3b2f2f;padding:10px;border-radius:8px">
        <h2 style="text-align:center;font-size:30px">BREAKOUT STOCK</h2>

        <table width="100%" cellpadding="8" style="border-collapse:collapse;background:#111">
        <tr style="background:#222">
            <th>SYMBOL</th>
            <th>LTP</th>
            <th>%</th>
            <th>SIGNAL%</th>
            <th>TIME</th>
        </tr>
        {breakout_rows}
        </table>
    </div>

    <div style="background:#3b2f2f;padding:10px;border-radius:8px;margin-top:30px">
        <h2 style="text-align:center;font-size:30px">INTRADAY BOOST</h2>

        <table width="100%" cellpadding="8" style="border-collapse:collapse;background:#111">
        <tr style="background:#222">
            <th>SYMBOL</th>
            <th>LTP</th>
            <th>%</th>
            <th>SIGNAL%</th>
            <th>TIME</th>
        </tr>
        {intraday_rows}
        </table>
    </div>

    </body>
    </html>
    """
