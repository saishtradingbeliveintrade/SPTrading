from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from services.market_data import scan_all_stocks

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def home():

    breakout, intraday = scan_all_stocks()

    def row(item):
        color_pct = "#00ff9d" if item["pct"] >= 0 else "#ff4d4d"
        color_sig = "#00ff9d" if item["signal"] >= 0 else "#ff4d4d"

        return f"""
        <div class='row'>
            <div class='c1'>
                <a href="https://www.tradingview.com/chart/?symbol=NSE:{item['symbol']}" target="_blank">
                    {item['symbol']}
                </a>
            </div>
            <div class='c2'>₹ {item['ltp']}</div>
            <div class='c3' style='color:{color_pct}'>{item['pct']}%</div>
            <div class='c4' style='color:{color_sig}'>{item['signal']}%</div>
            <div class='c5'>{item['time']}</div>
        </div>
        """

    html = f"""
    <html>
    <head>
    <style>
        body {{ background:#0b0b0b; font-family:Arial; color:white; padding:10px; }}
        .title {{ font-size:42px; font-weight:bold; text-align:center;
                  background:linear-gradient(90deg,cyan,lime);
                  padding:15px; border-radius:10px; margin-bottom:20px; }}
        .box-title {{ background:#c6a96b; color:black; font-size:28px;
                      font-weight:bold; text-align:center; padding:10px;
                      border-radius:8px; margin-top:25px; }}
        .header, .row {{ display:flex; padding:10px 5px; border-bottom:1px solid #222; }}
        .header {{ background:#1a1a1a; font-weight:bold; }}
        .c1 {{width:25%}} .c2 {{width:20%}} .c3 {{width:15%}}
        .c4 {{width:20%}} .c5 {{width:20%}}
        a {{ color:white; text-decoration:none; font-weight:bold; }}
    </style>
    </head>
    <body>

    <div class="title">SPTraders</div>

    <div class="box-title">BREAKOUT STOCK</div>
    <div class="header">
        <div class='c1'>SYMBOL</div>
        <div class='c2'>LTP</div>
        <div class='c3'>%</div>
        <div class='c4'>SIGNAL%</div>
        <div class='c5'>TIME</div>
    </div>
    {''.join([row(x) for x in breakout])}

    <div class="box-title">INTRADAY BOOST</div>
    <div class="header">
        <div class='c1'>SYMBOL</div>
        <div class='c2'>LTP</div>
        <div class='c3'>%</div>
        <div class='c4'>SIGNAL%</div>
        <div class='c5'>TIME</div>
    </div>
    {''.join([row(x) for x in intraday])}

    </body>
    </html>
    """

    return HTMLResponse(content=html)
