from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import data_routes

app = FastAPI(
    title="MCA SMA Crossover API",
    version="1.0.0",
    description="Backend for SMA crossover strategy with Lumibot + Lightweight Charts"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://127.0.0.1:5173",   # Sometimes browsers resolve localhost differently
        "http://localhost:5174",
        "http://192.168.31.201:5173"  # Local network access (your phone)
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(data_routes.router)

@app.get("/health")
def health_check():
    """SImple health check endpoint"""
    return {"status": "ok"}