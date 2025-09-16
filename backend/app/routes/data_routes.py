import json
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from ..services.data_service import fetch_ohlcv, add_sma, generatesignals, apply_exit_rules

router = APIRouter()

@router.get("/data")
def get_data(
    symbol: str = Query(..., description="Ticker symbol, e.g., AAPL"),
    start: str = Query(None, description="YYYY-MM-DD"),
    end: str = Query(None, description="YYYY-MM-DD"),
    interval: str = Query("1d", description="yfinance interval, e.g., 1d, 1h, 15m"),
    market_type: str = Query("stocks", description="Asset type, e.g., stocks, cryptos"),
    #backtest: bool = Query(False, description="Run backtest and include stats/equity"),
    #save_readme: bool = Query(False, description="Append stats to README.md"),
    #tp_pct: float = Query(0.50, description="Take-profit threshold (0.50 = +50%)"),
    #sl_pct: float = Query(-0.01, description="Stop-loss threshold (-0.01 = -1%)"),
):  
    df = fetch_ohlcv(symbol, start, end, interval)
    #print(df.columns)
    #print(df.head(n=100))
    #return {"message":"Succcess!"}
    df = add_sma(df, interval=interval, market_type=market_type)

    #print(df.columns)
    #print(df.head(n=15))

    #Generating signals
    df = generatesignals(df)
    df = apply_exit_rules(df)

    # Reset index so Date is a column for JSON
    df = df.reset_index()
    df["Date"] = df["Date"].astype(str)  # Ensure ISO string for frontend

    return JSONResponse(content=json.loads(df.to_json(orient="records")))

    