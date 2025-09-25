# 📈 SMA20 / SMA50 Crossover Trading Visualizer

A full‑stack trading strategy visualization tool that implements a **Simple Moving Average (SMA) crossover** strategy using **SMA20** and **SMA50**.  
Built with a **FastAPI + pandas** backend for data processing and a **React** frontend powered by **lightweight‑charts v4** for interactive chart rendering.

---

## 🚀 Overview

This project demonstrates:
- **Trading Strategy Logic**: Buy/Sell signals generated when SMA20 crosses SMA50.
- **Backend**: Modular FastAPI service for fetching, cleaning, and processing OHLCV data.
- **Frontend**: React app with clean UI blocks for:
  - Symbol selection
  - Date range
  - Interval
  - Market type
- **Charting**: Lightweight‑charts v4 for smooth, performant candlestick and overlay rendering.

---

## 🛠 Tech Stack

| Layer       | Technology |
|-------------|------------|
| Backend     | FastAPI, pandas |
| Frontend    | React, Vite, lightweight‑charts v4 |
| Data        | Any OHLCV source (e.g., Yahoo Finance, Alpha Vantage, custom feed) |
| Styling     | CSS / Tailwind / Styled Components (choose your flavor) |
| Database    | (Planned) PostgreSQL for backtesting |

---

## 📂 Project Structure 

TRADINGEMA/
│
├─ 📁 backend/
│   │
│   ├─ 📁 app/
│   │   ├─ 📁 __pycache__/           # Python bytecode cache
│   │   ├─ 📁 routes/                # API route definitions
│   │   ├─ 📁 services/              # Data fetching & SMA logic
│   │   └─ 📄 main.py                 # FastAPI entry point
│   │
│   ├─ 📄 .env                        # Environment variables
│   ├─ 📄 .gitignore                  # Git ignore rules
│   └─ 📄 requirements.txt            # Python dependencies
│
├─ 📁 frontend/
│   │
│   ├─ 📁 node_modules/               # Installed npm packages
│   ├─ 📁 public/                     # Static assets
│   │
│   ├─ 📁 src/
│   │   ├─ 📁 assets/                 # Images, icons, fonts
│   │   ├─ 📁 components/             # React UI components
│   │   ├─ 📄 App.css                  # Global styles
│   │   ├─ 📄 App.jsx                  # Root React component
│   │   ├─ 📄 form.css                 # Form styling
│   │   ├─ 📄 index.css                # Base styles
│   │   └─ 📄 main.jsx                 # React entry point
│   │
│   ├─ 📄 .gitignore                  # Git ignore rules
│   ├─ 📄 eslint.config.js            # ESLint configuration
│   ├─ 📄 index.html                  # HTML template
│   ├─ 📄 package-lock.json           # NPM lockfile
│   └─ 📄 package.json                # NPM dependencies & scripts
│
└─ 📄 README.md                       # Project documentation


---

## ⚙️ Setup Instructions

### 1️⃣ Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 5000
```

### 2️⃣ Frontend
```bash
cd frontend
npm install
npm run dev
```
## 📈 Usage

1. **Start the backend** to serve SMA‑processed data as JSON:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```
2. **Run the frontend**
   ```bash
   cd frontend
   npm run dev
   ```
3. **In the app, select**:
- Symbol (e.g., AAPL, BTCUSDT)
- Date range
- Interval (1m, 1h, 1d)
- Market type (Stock, Crypto, etc.)
  
4. **View** :
- Candlestick chart
- SMA20 (short‑term) and SMA50 (long‑term) overlays
- Buy/Sell markers at crossover points

## 🔄 Frontend–Backend Integration Notes
- Data Format: Backend returns JSON with OHLCV + SMA20 + SMA50 arrays.
- Null Safety: Ensure SMA arrays align with OHLCV timestamps; pad with null where needed.
- Version Specific: lightweight‑charts v4 API differs from v5 — stick to v4 docs for series creation and marker placement.
  
### CORS Setup (FastAPI):
 ```bash 
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```


## 📌 Example API Response
```bash
{
  "symbol": "AAPL",
  "data": [
    {
      "time": "2025-09-01",
      "open": 190.5,
      "high": 192.0,
      "low": 189.8,
      "close": 191.2,
      "sma20": 190.8,
      "sma50": 189.5
    }
  ]
}

```

## 🧠 Future Improvements
- PostgreSQL Integration for storing historical OHLCV data and enabling backtesting of the SMA crossover strategy.
- Add EMA crossover option
- Multi‑symbol comparison
- Dark mode toggle

## 📸Images & Response
<img width="1919" height="1076" alt="image" src="https://github.com/user-attachments/assets/66bdccc5-e3d8-4a8f-b31b-46676e0a5f0a" /> | <img width="1689" height="992" alt="image" src="https://github.com/user-attachments/assets/a9dc8bac-9f78-498c-8409-7ebed9098e5d" />



