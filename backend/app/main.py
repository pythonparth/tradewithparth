from fastapi import FastAPI
#from fastapi.middleware.cors import CORSMiddleware
from app.routes import data_routes

app = FastAPI(
    title="MCA SMA Crossover API",
    version="1.0.0",
    description="Backend for SMA crossover strategy with Lumibot + Lightweight Charts"
)

app.include_router(data_routes.router)

@app.get("/health")
def health_check():
    """SImple health check endpoint"""
    return {"status": "ok"}