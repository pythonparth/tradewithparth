import os
import psycopg2
from psycopg2.extras import Json
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()

DB_PARAMS = {
    "host": os.getenv("POSTGRES_HOST"),
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "port": os.getenv("POSTGRES_PORT"),
    "sslmode": os.getenv("POSTGRES_SSLMODE", "require")
}

def ensure_table_exists():
    """Create backtest_results table if it doesn't exist."""
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS backtest_results (
            id SERIAL PRIMARY KEY,
            symbol TEXT NOT NULL,
            market_type TEXT NOT NULL,
            interval TEXT NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            total_trades INTEGER,
            win_rate NUMERIC(5,2),
            avg_profit_pct NUMERIC(6,3),
            max_drawdown_pct NUMERIC(6,3),
            final_return_pct NUMERIC(6,3),
            exit_reason_counts JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def summarize_results(df: pd.DataFrame, symbol: str, market_type: str, interval: str, start_date: str, end_date: str):
    total_trades = int(df["BUY_SIGNAL"].sum())
    profitable_trades = int((df["EXIT_REASON"] == "take_profit").sum())
    win_rate = float(round((profitable_trades / total_trades * 100), 2)) if total_trades > 0 else 0.0
    avg_profit_pct = float(0)  # Optional: compute per-trade profit if tracking entry/exit
    max_drawdown_pct = float(round(((df["Close"].cummax() - df["Close"]) / df["Close"].cummax() * 100).max(), 3))
    final_return_pct = float(round(((df["Close"].iloc[-1] - df["Close"].iloc[0]) / df["Close"].iloc[0] * 100), 3))
    exit_reason_counts = df["EXIT_REASON"].value_counts().to_dict()

    return {
        "symbol": str(symbol),
        "market_type": str(market_type),
        "interval": str(interval),
        "start_date": str(start_date),
        "end_date": str(end_date),
        "total_trades": int(total_trades),
        "win_rate": float(win_rate),
        "avg_profit_pct": float(avg_profit_pct),
        "max_drawdown_pct": float(max_drawdown_pct),
        "final_return_pct": float(final_return_pct),
        "exit_reason_counts": exit_reason_counts,
        "created_at": datetime.utcnow()
    }

def insert_backtest_result(summary: dict):
    ensure_table_exists()
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO backtest_results (
            symbol, market_type, interval, start_date, end_date,
            total_trades, win_rate, avg_profit_pct, max_drawdown_pct,
            final_return_pct, exit_reason_counts, created_at
        ) VALUES (
            %(symbol)s, %(market_type)s, %(interval)s, %(start_date)s, %(end_date)s,
            %(total_trades)s, %(win_rate)s, %(avg_profit_pct)s, %(max_drawdown_pct)s,
            %(final_return_pct)s, %(exit_reason_counts)s, %(created_at)s
        )
    """, {**summary, "exit_reason_counts": Json(summary["exit_reason_counts"])})
    conn.commit()
    cur.close()
    conn.close()