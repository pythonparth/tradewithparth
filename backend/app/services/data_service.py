import pandas as pd
import numpy as np
import yfinance as yf

def fetch_ohlcv(symbol, start, end, interval):
    """
    Fetch OHLCV data from yahoo finance
    
    """
    #check statement for start < end
    if start and end:
        if pd.to_datetime(start) >= pd.to_datetime(end):
            #check statment for swapping
            start, end = end, start  # swap if out of order

    
    df = yf.download(
        symbol,
        start = start,
        end = end,
        interval = interval,
        auto_adjust=False,
        progress = False
    )
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]  # take only first level

    if df.empty:
        raise ValueError(f"No data for {symbol}")
    
    #Normalizing columns and index
    df = df.rename(columns=str.title)
    df.index = pd.to_datetime(df.index)
    if df.index.tz is not None:
        df.index = df.index.tz_localize(None)
    
    return df[['Open', 'High', 'Low', 'Close', 'Volume']].dropna()



def add_sma(df, interval="1d", market_type="stocks"):
    df = df.copy()

    if market_type == "stocks":
        bars_per_day = {
            "1d": 1, "1h": 6.5, "30m": 13, "15m": 26, "5m": 78, "1m": 390
        }
    else: #forex/crypto
        bars_per_day = {
            "1d": 1, "1h": 24, "30m": 48, "15m": 96, "5m": 288, "1m": 1440
        }
    bpd = bars_per_day.get(interval, 1)

    short_window = int(20*bpd)
    long_window = int(50*bpd)

    if "Close" not in df.columns:
        raise ValueError("DataFrame must contain a 'Close' column to calculate SMAs.")

    # For plotting
    df["SMA_20_plot"] = df["Close"].rolling(20, min_periods=1).mean()
    df["SMA_50_plot"] = df["Close"].rolling(50, min_periods=1).mean()

    # For signals
    df["SMA_20"] = df["Close"].rolling(20).mean()
    df["SMA_50"] = df["Close"].rolling(50).mean()

    # Generate signals only where both SMAs are valid
    #df["BUY_SIGNAL"] = (df["SMA_20"] > df["SMA_50"]) & df["SMA_50"].notna()
    return df


def generatesignals(df):
    df =df.copy()
    if not {"SMA_20", "SMA_50"}.issubset(df.columns):
        raise ValueError("Data Frame must contain 'SMA_20' & 'SMA_50' coulumns.")
    
    valid_mask = df["SMA_50"].notna()

    #Create boolean masks for crossovers

    crossover_up = (df["SMA_20"] > df["SMA_50"]) & (df["SMA_20"].shift(1) <= df["SMA_50"].shift(1))
    crossover_down = (df["SMA_20"] < df["SMA_50"]) & (df["SMA_20"].shift(1) >= df["SMA_50"].shift(1))

    #Applying masks only where SMA's are valid

    df["BUY_SIGNAL"] = crossover_up & valid_mask
    df["SELL_SIGNAL"] = crossover_down & valid_mask

    return df
    
def apply_exit_rules(df: pd.DataFrame,
                     stop_loss_pct: float = 0.01,
                     take_profit_pct: float = 0.50) -> pd.DataFrame:
    """
    Adds EXIT_SIGNAL, POSITION, and EXIT_REASON columns.
    EXIT_REASON is one of: 'stop_loss', 'take_profit', 'sell_signal', or None.
    """
    df = df.copy()
    
    if not {"Close", "BUY_SIGNAL", "SELL_SIGNAL"}.issubset(df.columns):
        raise ValueError("DataFrame must contain Close, BUY_SIGNAL, SELL_SIGNAL columns.")

    position = 0
    entry_price = None
    positions = []
    exit_signals = []
    exit_reasons = []

    for _, row in df.iterrows():
        if position == 0:
            if row["BUY_SIGNAL"]:
                position = 1
                entry_price = row["Close"]
                positions.append(1)
                exit_signals.append(False)
                exit_reasons.append(None)
            else:
                positions.append(0)
                exit_signals.append(False)
                exit_reasons.append(None)
        else:
            # SELL_SIGNAL exit (highest priority)
            if row["SELL_SIGNAL"]:
                position = 0
                entry_price = None
                positions.append(0)
                exit_signals.append(True)
                exit_reasons.append("sell_signal")

            # Stop-loss exit
            elif row["Close"] <= entry_price * (1 - stop_loss_pct):
                position = 0
                entry_price = None
                positions.append(0)
                exit_signals.append(True)
                exit_reasons.append("stop_loss")

            # Take-profit exit
            elif row["Close"] >= entry_price * (1 + take_profit_pct):
                position = 0
                entry_price = None
                positions.append(0)
                exit_signals.append(True)
                exit_reasons.append("take_profit")

            # Stay in trade
            else:
                positions.append(1)
                exit_signals.append(False)
                exit_reasons.append(None)

    df["POSITION"] = positions
    df["EXIT_SIGNAL"] = exit_signals
    df["EXIT_REASON"] = exit_reasons
    return df

