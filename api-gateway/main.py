import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import BANKING_SERVICE_URL
from app.routers.proxy import router

app = FastAPI(
    title="Banking API Gateway",
    description="API Gateway for Digital Banking System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="", tags=["API Gateway"])


@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "gateway running",
        "banking_service": BANKING_SERVICE_URL,
    }