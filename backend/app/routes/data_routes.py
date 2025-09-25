import json
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from ..services.data_service import fetch_ohlcv, add_sma, generatesignals, apply_exit_rules
from ..services.db_service import summarize_results, insert_backtest_result
router = APIRouter()

@router.get("/data")
def get_data(
    symbol: str = Query(..., description="Ticker symbol, e.g., AAPL"),
    start: str = Query(None, description="YYYY-MM-DD"),
    end: str = Query(None, description="YYYY-MM-DD"),
    interval: str = Query("1d", description="yfinance interval, e.g., 1d, 1h, 15m"),
    market_type: str = Query("stocks", description="Asset type, e.g., stocks, cryptos"),
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

    # Add Signal column for frontend markers (non-destructive)
    df = df.copy()
    df["Signal"] = None
    df.loc[df["BUY_SIGNAL"] == True, "Signal"] = "buy"
    df.loc[df["SELL_SIGNAL"] == True, "Signal"] = "sell"
    
    insert_backtest_result(summarize_results(
        df, symbol, market_type, interval, start, end)
    )
    # Reset index so Date is a column for JSON
    df = df.reset_index()
    df["Date"] = df["Date"].astype(str)  # Ensure ISO string for frontend

    return JSONResponse(content=json.loads(df.to_json(orient="records")))

    